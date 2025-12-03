"""
Ejemplo de uso del Vinted Scraper
Muestra diferentes formas de usar el scraper
"""

from scraper import VintedScraper
import json


def ejemplo_basico():
    """Ejemplo básico de scraping"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Scraping básico")
    print("="*60)

    scraper = VintedScraper(max_products=20)
    products = scraper.scrape()

    print(f"\n✓ Extraídos {len(products)} productos")

    # Guardar datos
    scraper.save_to_json()
    scraper.save_to_csv()

    print("✓ Datos guardados en JSON y CSV")


def ejemplo_con_callback():
    """Ejemplo con callback de progreso"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Scraping con progreso")
    print("="*60)

    def mostrar_progreso(current, total, message):
        porcentaje = (current / total * 100) if total > 0 else 0
        print(f"[{porcentaje:5.1f}%] {current}/{total} - {message}")

    scraper = VintedScraper(
        max_products=30,
        progress_callback=mostrar_progreso
    )

    products = scraper.scrape()
    print(f"\n✓ Completado: {len(products)} productos")


def ejemplo_analisis_datos():
    """Ejemplo de análisis de datos extraídos"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Análisis de datos")
    print("="*60)

    # Cargar datos del JSON
    try:
        with open('data/productos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            products = data.get('products', [])

        if not products:
            print("❌ No hay datos disponibles. Ejecuta el scraper primero.")
            return

        print(f"\n📊 Análisis de {len(products)} productos:\n")

        # Análisis de marcas
        marcas = {}
        for p in products:
            marca = p.get('brand', 'N/A')
            marcas[marca] = marcas.get(marca, 0) + 1

        print("🏷️  Top 5 Marcas:")
        for marca, count in sorted(marcas.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   - {marca}: {count} productos")

        # Análisis de precios
        precios = []
        for p in products:
            try:
                precio_str = p.get('price', '0').replace('€', '').replace(',', '.').strip()
                precio = float(precio_str.split()[0])
                precios.append(precio)
            except:
                pass

        if precios:
            print(f"\n💰 Análisis de precios:")
            print(f"   - Precio medio: {sum(precios)/len(precios):.2f} €")
            print(f"   - Precio mínimo: {min(precios):.2f} €")
            print(f"   - Precio máximo: {max(precios):.2f} €")

        # Análisis de estados
        estados = {}
        for p in products:
            estado = p.get('condition', 'N/A')
            estados[estado] = estados.get(estado, 0) + 1

        print(f"\n📦 Distribución por estado:")
        for estado, count in sorted(estados.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (count / len(products) * 100)
            print(f"   - {estado}: {count} ({porcentaje:.1f}%)")

    except FileNotFoundError:
        print("❌ Archivo de datos no encontrado. Ejecuta el scraper primero.")
    except Exception as e:
        print(f"❌ Error analizando datos: {e}")


def ejemplo_busqueda_especifica():
    """Ejemplo de scraping con búsqueda específica"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Búsqueda específica")
    print("="*60)

    # Puedes modificar la URL para buscar productos específicos
    scraper = VintedScraper(max_products=25)

    # Ejemplo: buscar zapatillas
    # url = "https://www.vinted.es/catalog?search_text=zapatillas"

    # Ejemplo: buscar por categoría
    # url = "https://www.vinted.es/catalog?category_id=123"

    print("\n💡 Tip: Modifica la URL en scraper.scrape(url='...') para buscar")
    print("   productos específicos, categorías o términos de búsqueda.")


def menu():
    """Menú interactivo"""
    print("\n" + "="*60)
    print("🛍️  VINTED SCRAPER - EJEMPLOS DE USO")
    print("="*60)
    print("\n1. Scraping básico (20 productos)")
    print("2. Scraping con progreso (30 productos)")
    print("3. Analizar datos existentes")
    print("4. Información sobre búsquedas específicas")
    print("5. Ejecutar todos los ejemplos")
    print("0. Salir")

    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        ejemplo_basico()
    elif opcion == "2":
        ejemplo_con_callback()
    elif opcion == "3":
        ejemplo_analisis_datos()
    elif opcion == "4":
        ejemplo_busqueda_especifica()
    elif opcion == "5":
        ejemplo_basico()
        ejemplo_con_callback()
        ejemplo_analisis_datos()
    elif opcion == "0":
        print("\n👋 ¡Hasta luego!")
        return
    else:
        print("\n❌ Opción inválida")

    input("\nPresiona Enter para continuar...")
    menu()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
