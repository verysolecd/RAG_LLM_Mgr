@echo off
chcp 65001 >nul
title ModelScope GGUF Downloader - Auto Start

echo ===================================================
echo     ModelScope GGUF Batch Downloader
echo ===================================================
echo.
echo [1/3] Checking environment...

cd /d "%~dp0"

IF NOT EXIST ".venv\Scripts\python.exe" (
    echo [X] Error: Virtual environment not found. Please ensure you have created it in this folder.
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/3] Starting download script (dl.py)...
echo.
echo ---------------------------------------------------
python gguf_dl\dl.py
echo ---------------------------------------------------

echo.
echo [√] All tasks finished or stopped.
pause
