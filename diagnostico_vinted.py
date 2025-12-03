"""
Script de diagnostico para inspeccionar la estructura de Vinted
"""

from playwright.sync_api import sync_playwright
import time

print("="*60)
print("DIAGNOSTICANDO ESTRUCTURA DE VINTED.ES")
print("="*60)

with sync_playwright() as p:
    print("\n[1/4] Iniciando navegador...")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()

    print("[2/4] Navegando a Vinted.es...")
    page.goto("https://www.vinted.es/catalog", wait_until='networkidle', timeout=60000)

    print("[3/4] Esperando a que carguen los productos...")
    time.sleep(5)

    # Cerrar cookies si aparecen
    try:
        cookie_button = page.query_selector('[id*="onetrust"], [class*="cookie"] button, .cookie-notice__button')
        if cookie_button:
            cookie_button.click()
            time.sleep(2)
    except:
        pass

    print("[4/4] Inspeccionando estructura HTML...\n")

    # Intentar encontrar contenedores de productos
    print("Buscando contenedores de productos:")
    selectors_to_try = [
        'div[data-testid="item-box"]',
        '.feed-grid__item',
        'div.new-item-box',
        'div[class*="item"]',
        'article',
        'div[class*="ItemBox"]',
        'div[class*="ItemCard"]'
    ]

    for selector in selectors_to_try:
        elements = page.query_selector_all(selector)
        print(f"  {selector}: {len(elements)} elementos")

        if len(elements) > 0:
            print(f"\n  OK ENCONTRADO! Usando: {selector}")
            print(f"  Analizando primer elemento...\n")

            first_elem = elements[0]
            html = first_elem.inner_html()

            # Guardar HTML para inspección
            with open('data/producto_ejemplo.html', 'w', encoding='utf-8') as f:
                f.write(html)

            print("  HTML guardado en: data/producto_ejemplo.html")

            # Intentar extraer texto
            print(f"\n  Texto completo del elemento:")
            print("  " + "-"*50)
            text = first_elem.inner_text()
            for line in text.split('\n')[:10]:
                print(f"  {line}")
            print("  " + "-"*50)

            # Buscar enlaces
            links = first_elem.query_selector_all('a')
            print(f"\n  Enlaces encontrados: {len(links)}")
            if len(links) > 0:
                print(f"  Primer enlace: {links[0].get_attribute('href')}")

            # Buscar imágenes
            imgs = first_elem.query_selector_all('img')
            print(f"\n  Imagenes encontradas: {len(imgs)}")
            if len(imgs) > 0:
                print(f"  Primera imagen: {imgs[0].get_attribute('src')[:80]}...")

            # Buscar precios (patrones comunes)
            print(f"\n  Buscando elementos de precio:")
            price_selectors = [
                '[data-testid*="price"]',
                '[class*="price"]',
                '[class*="Price"]',
                'span[class*="money"]',
                'div[class*="amount"]'
            ]

            for ps in price_selectors:
                price_elems = first_elem.query_selector_all(ps)
                if len(price_elems) > 0:
                    print(f"    {ps}: {len(price_elems)} elementos")
                    print(f"      Texto: {price_elems[0].inner_text()}")

            break

    print("\n" + "="*60)
    print("DIAGNOSTICO COMPLETADO")
    print("="*60)
    print("\nRevisa el archivo: data/producto_ejemplo.html")
    print("El navegador permanecera abierto 30 segundos para inspeccion manual")
    print("="*60)

    time.sleep(30)
    browser.close()
