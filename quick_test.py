from playwright.sync_api import sync_playwright
import time
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Navegando a Vinted...")
    page.goto("https://www.vinted.es/catalog", wait_until='networkidle', timeout=60000)

    time.sleep(5)

    # Cerrar cookies
    try:
        page.click('[id*="onetrust-accept"]', timeout=3000)
    except:
        pass

    time.sleep(2)

    # Buscar items
    items = page.query_selector_all('.feed-grid__item')
    print(f"Items encontrados: {len(items)}")

    if len(items) > 0:
        first = items[0]

        # Guardar HTML
        with open('data/item_html.txt', 'w', encoding='utf-8') as f:
            f.write(first.inner_html())

        # Extraer info
        info = {
            'texto_completo': first.inner_text(),
            'html_preview': first.inner_html()[:500]
        }

        # Enlaces
        link = first.query_selector('a')
        if link:
            info['url'] = link.get_attribute('href')

        # Imagen
        img = first.query_selector('img')
        if img:
            info['imagen'] = img.get_attribute('src')

        print(json.dumps(info, indent=2, ensure_ascii=False))

        with open('data/item_info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

    print("\nHTML guardado en: data/item_html.txt")
    print("Info guardada en: data/item_info.json")

    time.sleep(5)
    browser.close()
