1. proxy_git+pip+conda.sh
- PROXY_HOST=127.0.0.1 PROXY_PORT=10808 USE_SOCKS=0 bash proxy_git+pip+conda.sh #默认USE_SOCKS=0走http。USE_SOCKS=1走socks

2. unproxy_git+pip+conda.sh
- ./unproxy_git+pip+conda.sh

3. proxy_vscode.sh
- PROXY_PORT=10808 ./proxy_vscode.sh

4. unproxy_vscode.sh
- ./unproxy_vscode.sh
- pkill -f "code" ; code #重启Vscode

5. proxy_docker.sh
- PROXY_HOST=$(hostname -I | awk '{print $1}') PROXY_PORT=10808 PROXY_TYPE=http bash proxy_docker.sh

6. unproxy_docker.sh
- ./unproxy_docker.sh