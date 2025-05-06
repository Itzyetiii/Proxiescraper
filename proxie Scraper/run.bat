@echo off
title Proxy Scraper by @itzyetiii
cls
echo ================================================
echo   Proxy Scraper Installer and Runner
echo   by @itzyetiii on Twitch
echo ================================================
echo.

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Python not found. Please install Python first.
    pause
    exit /b
)

echo [*] Installing requirements...
pip install requests beautifulsoup4 pyfiglet

echo [*] Running Proxy Scraper...
python proxy_scraper.py
