#!/usr/bin/env bash
# ---------------------------------------------------------
# 关闭 Docker 代理（移除 /etc/systemd/system/docker.service.d/proxy.conf）
# 作者：Ming
# 用法：
#   bash disable_docker_proxy.sh
# ---------------------------------------------------------

set -e

DOCKER_PROXY_DIR="/etc/systemd/system/docker.service.d"
DOCKER_PROXY_FILE="$DOCKER_PROXY_DIR/proxy.conf"

echo "[INFO] Disabling Docker proxy..."

if [ -f "$DOCKER_PROXY_FILE" ]; then
    sudo rm -f "$DOCKER_PROXY_FILE"
    echo "[OK] Removed Docker proxy configuration: $DOCKER_PROXY_FILE"
else
    echo "[WARN] No proxy.conf found, nothing to remove."
fi

echo "[INFO] Reloading systemd daemon and restarting Docker..."
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "[INFO] Docker proxy has been disabled successfully."
systemctl show --property=Environment docker | grep -E "PROXY" || echo "[OK] No proxy environment detected."

echo "[DONE] ✅"

