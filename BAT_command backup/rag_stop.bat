@echo off
chcp 65001 >nul
echo ========================================
echo 正在停止旧进程，避免端口冲突...
echo ========================================



:: 2. 停止旧 llama-server
echo [2/6] 停止 llama-server 旧进程...
taskkill /f /im llama-server.exe >nul 2>&1

:: 3. 停止旧 RAGFlow Docker 容器
echo [3/6] 停止 RAGFlow 旧容器...
cd /d "D:\Dockers_data\Docker_RAGFLOW\ragflow\docker"
docker-compose down >nul 2>&1

:: 4. 停止旧 Nginx Proxy Manager 容器
echo [4/6] 停止 Nginx Proxy Manager 旧容器...
cd /d "D:\Dockers_data\Docker_NginxPM"
docker-compose down >nul 2>&1
