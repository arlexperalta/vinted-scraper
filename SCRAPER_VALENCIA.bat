@echo off
echo ============================================================
echo  VINTED SCRAPER - ROPA EN VALENCIA
echo ============================================================
echo.
echo Este script busca SOLO ropa cerca de Valencia, Espana
echo.
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe scraper_valencia.py

pause
