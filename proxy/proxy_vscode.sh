#!/usr/bin/env bash
set -euo pipefail

PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-10808}"
HTTP_URL="http://${PROXY_HOST}:${PROXY_PORT}"

SETTINGS="${HOME}/.config/Code/User/settings.json"
mkdir -p "$(dirname "$SETTINGS")"
[[ -f "$SETTINGS" ]] || echo '{}' > "$SETTINGS"

apply_with_jq() {
  local tmp; tmp="$(mktemp)"
  jq '. + {"http.proxy":"'"$HTTP_URL"'","http.proxySupport":"on"}' \
    "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"
}
apply_with_python() {
  python3 - "$SETTINGS" "$HTTP_URL" <<'PY'
import json,sys,os
p, proxy = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(p,'r',encoding='utf-8'))
except Exception:
    data = {}
data["http.proxy"] = proxy
data["http.proxySupport"] = "on"
tmp = p + ".tmp"
json.dump(data, open(tmp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
os.replace(tmp, p)
PY
}

if command -v jq >/dev/null 2>&1; then apply_with_jq; else apply_with_python >/dev/null; fi
echo "[VSCode] settings.json -> http.proxy: $HTTP_URL, proxySupport: on"

