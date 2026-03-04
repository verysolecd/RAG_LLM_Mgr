@echo off
chcp 65001 >nul
title Create and Run Qwen Mod

echo ========================================
echo 正在基于 mod_qwen3 创建定制大语言模型...
echo ========================================
ollama create qwen3.5_mod -f mod_qwen3

echo.
echo ========================================
echo 模型创建完成，正在启动运行...
echo ========================================
ollama run qwen3.5_mod

pause
