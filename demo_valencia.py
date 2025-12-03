"""
Demo automatica del scraper de Valencia
Extrae 10 productos de ropa de mujer
"""

from scraper import VintedScraper
from config_filtros import construir_url_vinted

print("\n" + "="*70)
print(" DEMO: SCRAPING DE ROPA DE MUJER EN VALENCIA")
print("="*70)

# Construir URL con filtros
url = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    precio_max=30  # Max 30 euros para encontrar mas resultados
)

print(f"\nURL: {url}")
print("\nFiltros aplicados:")
print("  - Ubicacion: Valencia, Espana")
print("  - Categoria: Ropa de mujer")
print("  - Precio maximo: 30 EUR")
print("\n" + "-"*70)
print("Extrayendo 10 productos...")
print("-"*70 + "\n")

def mostrar_progreso(current, total, message):
    print(f"[{current}/{total}] {message[:60]}")

# Crear scraper
scraper = VintedScraper(max_products=10, progress_callback=mostrar_progreso)

try:
    # Ejecutar scraping
    productos = scraper.scrape(url=url)

    if productos:
        print("\n" + "="*70)
        print(f" EXITO! {len(productos)} PRODUCTOS ENCONTRADOS")
        print("="*70)

        # Mostrar todos los productos
        for i, p in enumerate(productos, 1):
            print(f"\n[{i}] {p['title']}")
            print(f"    Precio: {p['price']}")
            print(f"    Estado: {p['condition']}")
            print(f"    URL: {p['product_url']}")
            print(f"    Imagen: {p['image_url'][:70]}...")

        # Guardar datos
        scraper.save_to_json()
        scraper.save_to_csv()

        print("\n" + "="*70)
        print(" DATOS GUARDADOS")
        print("="*70)
        print("\n  JSON: data/productos.json")
        print("  CSV:  data/productos.csv")

        print("\n" + "="*70)
        print(" SIGUIENTE PASO")
        print("="*70)
        print("\n  Para explorar los productos con filtros:")
        print("  1. Ejecuta: INICIAR_WEB.bat")
        print("  2. Abre: http://localhost:5000")
        print("\n  O ejecuta SCRAPER_VALENCIA.bat para menu interactivo")
        print("="*70 + "\n")

    else:
        print("\nNo se encontraron productos")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
