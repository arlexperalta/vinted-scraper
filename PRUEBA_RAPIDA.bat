@echo off
echo ============================================================
echo  PRUEBA RAPIDA DEL SCRAPER (5 productos)
echo ============================================================
echo.
echo Esta prueba extraera 5 productos para verificar que funciona
echo.
echo ============================================================
echo.

cd /d "%~dp0"
venv\Scripts\python.exe test_scraper.py

echo.
echo ============================================================
echo Si viste los productos arriba, todo funciona correctamente!
echo Ahora puedes ejecutar INICIAR_WEB.bat para la interfaz web
echo ============================================================
pause
