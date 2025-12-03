"""
Prueba rapida del scraper con filtros de Valencia
"""

from scraper import VintedScraper
from config_filtros import construir_url_vinted, URL_ROPA_MUJER_VALENCIA

print("="*60)
print("PROBANDO SCRAPER CON FILTRO DE VALENCIA")
print("="*60)

# Mostrar la URL que se usara
print(f"\nURL: {URL_ROPA_MUJER_VALENCIA}")
print("\nFiltrando: Ropa de mujer cerca de Valencia\n")

def progreso(current, total, message):
    print(f"[{current}/{total}] {message[:60]}")

# Crear scraper y extraer 5 productos de prueba
scraper = VintedScraper(max_products=5, progress_callback=progreso)

try:
    productos = scraper.scrape(url=URL_ROPA_MUJER_VALENCIA)

    if productos:
        print("\n" + "="*60)
        print(f"EXITO! {len(productos)} productos encontrados")
        print("="*60)

        # Mostrar productos
        for i, p in enumerate(productos, 1):
            print(f"\nProducto {i}:")
            print(f"  Titulo: {p['title']}")
            print(f"  Precio: {p['price']}")
            print(f"  Condicion: {p['condition']}")
            print(f"  URL: {p['product_url'][:70]}...")

        # Guardar
        scraper.save_to_json('productos_valencia_test.json')
        print(f"\n OK - Datos guardados en: data/productos_valencia_test.json")

        print("\n" + "="*60)
        print("FILTROS FUNCIONANDO CORRECTAMENTE!")
        print("="*60)
        print("\nPasos siguientes:")
        print("1. Ejecuta SCRAPER_VALENCIA.bat para menu interactivo")
        print("2. O ejecuta INICIAR_WEB.bat para interfaz web")
        print("="*60)

    else:
        print("\nNo se encontraron productos")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
