@echo off
echo ============================================================
echo  VINTED SCRAPER - Modo directo
echo ============================================================
echo.
echo Ejecutando scraper...
echo Los datos se guardaran en la carpeta 'data/'
echo.
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe scraper.py

echo.
echo ============================================================
echo Scraping completado!
echo ============================================================
pause
