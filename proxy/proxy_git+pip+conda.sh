#!/usr/bin/env bash
set -euo pipefail

# ===== 配置：默认 HTTP 代理；需要可用环境变量覆盖 =====
PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-10808}"
USE_SOCKS="${USE_SOCKS:-0}"          # 0=HTTP(默认)；1=SOCKS5
HTTP_URL="http://${PROXY_HOST}:${PROXY_PORT}"
SOCKS_URL="socks5h://${PROXY_HOST}:${PROXY_PORT}"

echo "[Proxy] $( [[ $USE_SOCKS == 1 ]] && echo "$SOCKS_URL (SOCKS5)" || echo "$HTTP_URL (HTTP)" )"

# ===== 1) 设置 Git / Pip / Conda 的代理（永久）=====
if command -v git >/dev/null 2>&1; then
  if [[ "$USE_SOCKS" == "1" ]]; then
    git config --global http.proxy  "$SOCKS_URL"
    git config --global https.proxy "$SOCKS_URL"
  else
    git config --global http.proxy  "$HTTP_URL"
    git config --global https.proxy "$HTTP_URL"
  fi
  echo "[Git ] proxy set"
else
  echo "[Git ] git not found (skipped)"
fi

if command -v pip >/dev/null 2>&1; then
  if [[ "$USE_SOCKS" == "1" ]]; then
    pip config set global.proxy "$SOCKS_URL" >/dev/null
  else
    pip config set global.proxy "$HTTP_URL" >/dev/null
  fi
  echo "[Pip ] proxy set"
else
  echo "[Pip ] pip not found (skipped)"
fi

if command -v conda >/dev/null 2>&1; then
  if [[ "$USE_SOCKS" == "1" ]]; then
    conda config --set proxy_servers.http  "$SOCKS_URL"
    conda config --set proxy_servers.https "$SOCKS_URL"
  else
    conda config --set proxy_servers.http  "$HTTP_URL"
    conda config --set proxy_servers.https "$HTTP_URL"
  fi
  echo "[Conda] proxy set"
else
  echo "[Conda] conda not found (skipped)"
fi

# ===== 2) 验证（仅本次进程临时注入代理环境）=====
set +e

# 注入临时环境变量以保证验证阶段都走代理
if [[ "$USE_SOCKS" == "1" ]]; then
  export ALL_PROXY="$SOCKS_URL"; export all_proxy="$SOCKS_URL"
  unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
else
  export HTTP_PROXY="$HTTP_URL"; export HTTPS_PROXY="$HTTP_URL"
  export http_proxy="$HTTP_URL"; export https_proxy="$HTTP_URL"
  unset ALL_PROXY all_proxy
fi
export NO_PROXY="localhost,127.0.0.1,::1,*.local"
export no_proxy="$NO_PROXY"

# -- Git: 拉取 refs --
if command -v git >/dev/null 2>&1; then
  timeout 10s git ls-remote -q https://github.com/NVlabs/tiny-cuda-nn.git >/dev/null 2>&1
  [[ $? -eq 0 ]] && echo "[Check][Git ] OK" || echo "[Check][Git ] FAIL"
fi

# -- Pip: 下载一个小包（无依赖） --
if command -v pip >/dev/null 2>&1; then
  tmpdir="$(mktemp -d)"
  timeout 10s pip download -q --retries 1 --timeout 10 --no-deps -d "$tmpdir" requests >/dev/null 2>&1
  [[ $? -eq 0 && -n "$(ls -A "$tmpdir" 2>/dev/null)" ]] && echo "[Check][Pip ] OK" || echo "[Check][Pip ] FAIL"
  rm -rf "$tmpdir" >/dev/null 2>&1
fi

# -- Conda: 更稳健的双探针 + 更长超时 --
if command -v conda >/dev/null 2>&1; then
  CONDATIMEOUT="${CONDATIMEOUT:-45}"
  conda clean -y --index-cache >/dev/null 2>&1 || true

  timeout "${CONDATIMEOUT}s" conda search --override-channels -c conda-forge zlib --info >/dev/null 2>&1 \
  || timeout "${CONDATIMEOUT}s" conda search --override-channels -c defaults ca-certificates --info >/dev/null 2>&1

  if [[ $? -eq 0 ]]; then
    echo "[Check][Conda] OK"
  else
    echo "[Check][Conda] FAIL"
    # 打印当前代理配置，便于排错（不输出其它冗余）
    conda config --show proxy_servers 2>/dev/null | sed 's/^/[Conda] /'
  fi

  conda clean -y --index-cache >/dev/null 2>&1 || true
fi

set -e


