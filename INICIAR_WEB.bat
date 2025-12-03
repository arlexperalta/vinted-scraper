@echo off
echo ============================================================
echo  VINTED SCRAPER - Iniciando servidor web...
echo ============================================================
echo.
echo La interfaz web se abrira en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe app.py

pause
