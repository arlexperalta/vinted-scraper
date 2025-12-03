"""
Scraper de Vinted configurado para Valencia, España
Busca solo ropa cerca de Valencia
"""

from scraper import VintedScraper
from config_filtros import construir_url_vinted, URLS_EJEMPLO
import json


def mostrar_menu():
    """Muestra menu de opciones de busqueda"""
    print("\n" + "="*60)
    print("  VINTED SCRAPER - ROPA EN VALENCIA")
    print("="*60)
    print("\nSelecciona el tipo de ropa que quieres buscar:\n")
    print("1. Ropa de mujer")
    print("2. Ropa de hombre")
    print("3. Zapatos de mujer")
    print("4. Zapatos de hombre")
    print("5. Toda la ropa (economica, max 20€)")
    print("6. Ropa en muy buen estado")
    print("7. Busqueda personalizada")
    print("0. Salir")
    print("="*60)


def obtener_url_por_opcion(opcion):
    """Retorna la URL segun la opcion elegida"""
    urls = {
        "1": construir_url_vinted("es", "ropa_mujer", "valencia"),
        "2": construir_url_vinted("es", "ropa_hombre", "valencia"),
        "3": construir_url_vinted("es", "zapatos_mujer", "valencia"),
        "4": construir_url_vinted("es", "zapatos_hombre", "valencia"),
        "5": construir_url_vinted("es", "toda_ropa", "valencia", precio_max=20),
        "6": construir_url_vinted("es", "toda_ropa", "valencia", estado="muy_bueno"),
    }

    return urls.get(opcion)


def busqueda_personalizada():
    """Permite crear una busqueda personalizada"""
    print("\n" + "="*60)
    print("  BUSQUEDA PERSONALIZADA")
    print("="*60)

    # Categoria
    print("\nCategoria:")
    print("1. Ropa de mujer")
    print("2. Ropa de hombre")
    print("3. Zapatos de mujer")
    print("4. Zapatos de hombre")
    print("5. Accesorios")
    print("6. Todo")

    cat_map = {
        "1": "ropa_mujer",
        "2": "ropa_hombre",
        "3": "zapatos_mujer",
        "4": "zapatos_hombre",
        "5": "accesorios",
        "6": "toda_ropa"
    }

    cat_input = input("\nElige categoria (1-6): ").strip()
    categoria = cat_map.get(cat_input, "ropa_mujer")

    # Precio maximo
    precio_max = input("\nPrecio maximo en € (Enter para sin limite): ").strip()
    precio_max = int(precio_max) if precio_max.isdigit() else None

    # Busqueda de texto
    busqueda = input("\nBuscar palabra clave (Enter para omitir): ").strip()
    busqueda = busqueda if busqueda else None

    # Estado
    print("\nEstado:")
    print("1. Nuevo")
    print("2. Muy bueno")
    print("3. Bueno")
    print("4. Cualquiera")

    estado_map = {
        "1": "nuevo",
        "2": "muy_bueno",
        "3": "bueno",
        "4": None
    }

    estado_input = input("\nElige estado (1-4): ").strip()
    estado = estado_map.get(estado_input, None)

    # Construir URL
    url = construir_url_vinted(
        pais="es",
        categoria=categoria,
        ubicacion="valencia",
        precio_max=precio_max,
        busqueda=busqueda,
        estado=estado
    )

    print(f"\nURL generada: {url}")
    return url


def ejecutar_scraping(url, num_productos=20):
    """Ejecuta el scraping con la URL especificada"""
    print("\n" + "="*60)
    print(f"  INICIANDO SCRAPING - {num_productos} productos")
    print("="*60)
    print(f"\nURL: {url}\n")

    def progreso(current, total, message):
        print(f"[{current}/{total}] {message[:60]}")

    scraper = VintedScraper(max_products=num_productos, progress_callback=progreso)

    try:
        products = scraper.scrape(url=url)

        if products:
            print("\n" + "="*60)
            print(f"  EXITO! {len(products)} productos encontrados")
            print("="*60)

            # Mostrar resumen
            print("\nPRIMEROS 5 PRODUCTOS:")
            for i, p in enumerate(products[:5], 1):
                print(f"\n{i}. {p['title']}")
                print(f"   Precio: {p['price']} | Estado: {p['condition']}")
                print(f"   URL: {p['product_url'][:60]}...")

            # Guardar
            scraper.save_to_json()
            scraper.save_to_csv()

            print("\n" + "="*60)
            print("  DATOS GUARDADOS")
            print("="*60)
            print("\n  JSON: data/productos.json")
            print("  CSV:  data/productos.csv")
            print("\n  Abre la interfaz web para explorar los productos:")
            print("  python app.py")
            print("="*60)

            return True
        else:
            print("\nNo se encontraron productos con estos filtros")
            return False

    except Exception as e:
        print(f"\nERROR durante el scraping: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Funcion principal"""
    while True:
        mostrar_menu()
        opcion = input("\nElige una opcion (0-7): ").strip()

        if opcion == "0":
            print("\nSaliendo...")
            break

        elif opcion == "7":
            url = busqueda_personalizada()
        else:
            url = obtener_url_por_opcion(opcion)

        if url:
            # Preguntar cuantos productos
            num = input("\nCuantos productos quieres extraer? (default: 20): ").strip()
            num_productos = int(num) if num.isdigit() else 20

            # Ejecutar
            exito = ejecutar_scraping(url, num_productos)

            if exito:
                continuar = input("\nDeseas hacer otra busqueda? (s/n): ").strip().lower()
                if continuar != 's':
                    break
            else:
                reintentar = input("\nDeseas reintentar con otros filtros? (s/n): ").strip().lower()
                if reintentar != 's':
                    break
        else:
            print("\nOpcion no valida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario. Saliendo...")
    except Exception as e:
        print(f"\nError inesperado: {e}")
