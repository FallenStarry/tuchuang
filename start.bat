@echo off
chcp 65001
title 文件上传服务
cd /d "%~dp0/app"
python main.py
pause