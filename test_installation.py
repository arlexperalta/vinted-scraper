"""
Script de prueba para verificar la instalacion
"""

print("="*60)
print(" VERIFICANDO INSTALACION DE VINTED SCRAPER")
print("="*60)

# Test 1: Python
import sys
print(f"\n[1/5] Python version: {sys.version.split()[0]} - OK")

# Test 2: Playwright
try:
    from playwright.sync_api import sync_playwright
    print("[2/5] Playwright importado correctamente - OK")
except ImportError as e:
    print(f"[2/5] ERROR: Playwright no se pudo importar: {e}")
    sys.exit(1)

# Test 3: BeautifulSoup
try:
    from bs4 import BeautifulSoup
    print("[3/5] BeautifulSoup importado correctamente - OK")
except ImportError as e:
    print(f"[3/5] ERROR: BeautifulSoup no se pudo importar: {e}")
    sys.exit(1)

# Test 4: Flask
try:
    from flask import Flask
    print("[4/5] Flask importado correctamente - OK")
except ImportError as e:
    print(f"[4/5] ERROR: Flask no se pudo importar: {e}")
    sys.exit(1)

# Test 5: Scraper
try:
    from scraper import VintedScraper
    print("[5/5] Scraper importado correctamente - OK")
except ImportError as e:
    print(f"[5/5] ERROR: Scraper no se pudo importar: {e}")
    sys.exit(1)

print("\n" + "="*60)
print(" TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
print("="*60)
print("\nPasos siguientes:")
print("1. Ejecuta la interfaz web: python app.py")
print("2. Abre tu navegador en: http://localhost:5000")
print("3. Haz clic en 'Actualizar Datos' para comenzar el scraping")
print("\nO ejecuta directamente: python scraper.py")
print("="*60)
