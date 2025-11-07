#!/usr/bin/env bash
set -euo pipefail

# Git
if command -v git >/dev/null 2>&1; then
  git config --global --unset-all http.proxy  >/dev/null 2>&1 || true
  git config --global --unset-all https.proxy >/dev/null 2>&1 || true
  echo "[Git ] proxy unset"
else
  echo "[Git ] git not found (skipped)"
fi

# Pip
if command -v pip >/dev/null 2>&1; then
  # pip 有 unset 子命令；若不存在就覆盖为空
  if pip config unset global.proxy >/dev/null 2>&1; then
    :
  else
    pip config set global.proxy "" >/dev/null 2>&1 || true
  fi
  echo "[Pip ] proxy unset"
else
  echo "[Pip ] pip not found (skipped)"
fi

# Conda
if command -v conda >/dev/null 2>&1; then
  conda config --remove-key proxy_servers.http  >/dev/null 2>&1 || true
  conda config --remove-key proxy_servers.https >/dev/null 2>&1 || true
  echo "[Conda] proxy unset"
else
  echo "[Conda] conda not found (skipped)"
fi

