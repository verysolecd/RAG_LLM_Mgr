@echo off
echo Starting Services in Windows Terminal Tabs...

wt ^
    new-tab --title "Embedding (8001)" powershell -NoExit -Command "llama-server.exe -m '%MODEL_DIR%\bge-m3-q8_0.gguf' --host 0.0.0.0 --port 8088 --embedding -t 8" ^
    ; ^
    new-tab --title "Rerank (8080)" powershell -NoExit -Command "llama-server.exe -m '%MODEL_DIR%\bge-reranker-v2-m3-FP16.gguf' --host 0.0.0.0 --port 8000 --embedding --pooling rank --reranking -t 8"
