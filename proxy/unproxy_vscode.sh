#!/usr/bin/env bash
set -euo pipefail

SETTINGS="${HOME}/.config/Code/User/settings.json"
if [[ ! -f "$SETTINGS" ]]; then
  echo "[VSCode] settings.json not found (skipped)"
  exit 0
fi

clean_with_jq() {
  local tmp; tmp="$(mktemp)"
  jq 'del(.["http.proxy","http.proxySupport"])' "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"
}
clean_with_python() {
  python3 - "$SETTINGS" <<'PY'
import json,sys,os
p=sys.argv[1]
try:
    data=json.load(open(p,'r',encoding='utf-8'))
except Exception:
    data={}
for k in ["http.proxy","http.proxySupport"]:
    if k in data: del data[k]
tmp=p+".tmp"
json.dump(data, open(tmp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
os.replace(tmp,p)
PY
}

if command -v jq >/dev/null 2>&1; then clean_with_jq; else clean_with_python >/dev/null; fi
echo "[VSCode] settings.json proxy removed"

