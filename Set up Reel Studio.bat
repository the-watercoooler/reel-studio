@echo off
title Reel Studio set-up
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\setup-windows.ps1" %*
echo.
pause
