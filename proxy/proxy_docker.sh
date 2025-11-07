#!/usr/bin/env bash
# ============================================================
#  Docker Proxy Enabler
#  作者: 李佳潞
#  功能: 让 Docker 走 VPN 代理 (HTTP 或 SOCKS5)
# ============================================================

set -e

# ==== 参数定义 ====
PROXY_HOST=${PROXY_HOST:-127.0.0.1}
PROXY_PORT=${PROXY_PORT:-7890}   # Clash 默认7890, V2Ray 默认10809
PROXY_TYPE=${PROXY_TYPE:-http}   # 可选: http / socks5 / socks5h

echo "[INFO] Setting Docker proxy via ${PROXY_TYPE}://${PROXY_HOST}:${PROXY_PORT}"

# ==== 检查 Docker 是否安装 ====
if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] docker not found. Please install docker first."
  exit 1
fi

# ==== 创建 Docker 配置目录 ====
sudo mkdir -p /etc/systemd/system/docker.service.d

# ==== 写入代理配置 ====
cat <<EOF | sudo tee /etc/systemd/system/docker.service.d/proxy.conf >/dev/null
[Service]
Environment="HTTP_PROXY=${PROXY_TYPE}://${PROXY_HOST}:${PROXY_PORT}"
Environment="HTTPS_PROXY=${PROXY_TYPE}://${PROXY_HOST}:${PROXY_PORT}"
Environment="NO_PROXY=localhost,127.0.0.1,::1,*.local"
EOF

# ==== 重启 Docker 服务 ====
sudo systemctl daemon-reload
sudo systemctl restart docker

# ==== 验证配置 ====
echo "[INFO] Docker proxy environment:"
systemctl show --property=Environment docker

echo "[OK] Docker now uses ${PROXY_TYPE}://${PROXY_HOST}:${PROXY_PORT}"

