@echo off
echo Starting Services in Windows Terminal Tabs...

echo stop ollama and llama-server....
:: 强制结束所有 Ollama 进程（不管端口是否占用）
taskkill /F /IM ollama.exe >nul 2>&1
taskkill /F /IM ollama_service.exe >nul 2>&1
taskkill /F /IM llama-server.exe >nul 2>&1
taskkill /f /im ollama.exe ollama_service.exe >nul 2>&1
