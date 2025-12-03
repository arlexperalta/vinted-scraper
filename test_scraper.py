"""
Script de prueba rapida del scraper con 5 productos
"""

from scraper import VintedScraper
import json

print("="*60)
print("PROBANDO SCRAPER CON SELECTORES CORREGIDOS")
print("="*60)

def progreso(current, total, message):
    print(f"[{current}/{total}] {message[:60]}")

print("\nExtrayendo 5 productos de prueba...\n")

scraper = VintedScraper(max_products=5, progress_callback=progreso)

try:
    products = scraper.scrape()

    if products:
        print("\n" + "="*60)
        print(f"EXITO! Se extrajeron {len(products)} productos")
        print("="*60 + "\n")

        # Mostrar los productos
        for i, p in enumerate(products, 1):
            print(f"\nProducto {i}:")
            print(f"  Titulo: {p['title']}")
            print(f"  Precio: {p['price']}")
            print(f"  Condicion: {p['condition']}")
            print(f"  Marca: {p['brand']}")
            print(f"  Talla: {p['size']}")
            print(f"  URL: {p['product_url'][:60]}...")
            print(f"  Imagen: {p['image_url'][:60]}...")
            print(f"  Ubicacion: {p['location']}")

        # Guardar
        scraper.save_to_json('productos_test.json')
        print(f"\n✓ Datos guardados en: data/productos_test.json")

        # Verificar que los datos sean correctos
        print("\n" + "="*60)
        print("VERIFICACION:")
        print("="*60)

        issues = []
        for i, p in enumerate(products, 1):
            if p['title'] == "N/A":
                issues.append(f"Producto {i}: Titulo no encontrado")
            if p['price'] == "N/A":
                issues.append(f"Producto {i}: Precio no encontrado")
            if p['product_url'] == "":
                issues.append(f"Producto {i}: URL no encontrada")

        if issues:
            print("\nProblemas encontrados:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n✓ Todos los productos tienen datos validos!")

    else:
        print("\nERROR: No se extrajeron productos")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
