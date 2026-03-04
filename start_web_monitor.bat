@echo off
chcp 65001 >nul
title 启动 Web 监控面板

:: 使用当前目录下的专属 python 虚拟环境
set "PYTHON_CMD=%~dp0.venv\Scripts\python.exe"

echo ==============================================================
echo 正在启动 AI 模型 Web 监控面板 (本地端口: 8899)...
echo 运行环境: 独立本地环境 (.venv)
echo ==============================================================
echo.

:: 检查 Python 环境
if not exist "%PYTHON_CMD%" (
    echo [错误] 找不到自带的 Python 虚拟环境！
    echo 请检查 d:\oLLM\.venv 文件夹是否存在。
    pause
    exit
)

:: 后台运行 python 脚本
start "" "%PYTHON_CMD%" "%~dp0webmonitor\web_monitor.py"

:: 延迟 2 秒等待服务启动
ping 127.0.0.1 -n 3 >nul

:: 自动在浏览器打开网页
start http://127.0.0.1:8899
