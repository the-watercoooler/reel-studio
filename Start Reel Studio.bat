@echo off
title Reel Studio - keep this window open while editing
cd /d "%~dp0"
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
"%PY%" studio.py %*
if errorlevel 1 pause
