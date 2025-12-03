@echo off
echo ============================================================
echo  VERIFICANDO INSTALACION
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe test_installation.py

echo.
pause
