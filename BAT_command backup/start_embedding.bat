@echo off
title Embedding Service (8001)
echo Starting Embedding Service in PowerShell...
start powershell -NoExit -Command "llama-server.exe -m '%MODEL_DIR%\bge-m3-q8_0.gguf' --host 0.0.0.0 --port 8088 --embedding -t 8"
