@echo off
title Rerank Service (8000)
echo Starting Rerank Service in PowerShell...
start powershell -NoExit -Command "llama-server.exe -m '%MODEL_DIR%\bge-reranker-v2-m3-FP16.gguf' --host 0.0.0.0 --port 8000 --embedding --pooling rank --reranking -t 8"
