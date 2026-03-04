@echo off
chcp 65001 >nul
title 查看运行中的模型资源占用

:MENU
cls
:: 运行专用的 PowerShell 脚本来获取数据
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0check_models_core.ps1"

echo ==============================================================
echo  1. 刷新重试 
echo  2. 退出关闭 
echo ==============================================================
set /p user_cmd=请输入您的选择 (1 或 2): 

if "%user_cmd%"=="1" goto MENU
if "%user_cmd%"=="2" goto END

:: 输入错误时默认刷新
goto MENU

:END
exit
