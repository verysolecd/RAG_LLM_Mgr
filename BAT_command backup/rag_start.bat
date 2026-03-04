@echo off
chcp 65001 >nul
title 服务一键重启

echo 正在停止旧服务...

docker-compose -f "D:\Dockers_data\Docker_RAGFLOW\ragflow\docker\docker-compose.yml" down >nul 2>&1
docker-compose -f "D:\Dockers_data\Docker_NginxPM\docker-compose.yml" down >nul 2>&1

echo 正在启动新服务...

docker-compose -f "D:\Dockers_data\Docker_NginxPM\docker-compose.yml" up -d
docker-compose -f "D:\Dockers_data\Docker_RAGFLOW\ragflow\docker\docker-compose.yml" up -d
docker-compose -f "D:\Dockers_data\Docker_NginxPM\docker-compose.yml" up -d

echo ✅ 启动完成！
start chrome "http://rag.local"

echo.
echo 服务地址：
echo - Ollama: http://localhost:11434
echo - RAGFlow: http://rag.local
echo - Nginx PM: http://localhost:81
pause