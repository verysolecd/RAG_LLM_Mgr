# RAG Manager Setup Script for Windows
# This script automates the creation of a Python virtual environment and installs dependencies.

$ErrorActionPreference = "Stop"

Write-Host "--- RAG Manager Environment Setup ---" -ForegroundColor Cyan

# 1. Check for Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found Python: $pythonVersion"
} catch {
    Write-Host "[ERROR] Python not found in PATH. Please install Python 3.8+." -ForegroundColor Red
    exit
}

# 2. Create Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Successfully created .venv" -ForegroundColor Green
} else {
    Write-Host "Virtual environment (.venv) already exists." -ForegroundColor Gray
}

# 3. Install Dependencies
Write-Host "Installing/Updating dependencies from requirements.txt..." -ForegroundColor Yellow
& .venv\Scripts\pip.exe install --upgrade pip
& .venv\Scripts\pip.exe install -r requirements.txt

Write-Host "`nSetup Complete!" -ForegroundColor Green
Write-Host "You can now run the monitor using: .\start_web_monitor.bat" -ForegroundColor Cyan
Pause
