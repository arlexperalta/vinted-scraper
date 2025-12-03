@echo off
echo ============================================================
echo  PRUEBA RAPIDA - FILTRO VALENCIA
echo ============================================================
echo.
echo Extrayendo 5 productos de ropa cerca de Valencia...
echo.
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe test_valencia.py

echo.
pause
