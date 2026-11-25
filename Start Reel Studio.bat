@echo off
title Reel Studio - keep this window open while editing
cd /d "%~dp0"
python studio.py
if errorlevel 1 pause
