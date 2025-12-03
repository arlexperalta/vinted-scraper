"""
Vinted.es Web Scraper
Extrae productos de Vinted usando Playwright
"""

import json
import csv
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Callable
from playwright.sync_api import sync_playwright, Page, Browser
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VintedScraper:
    """Scraper para extraer productos de Vinted.es"""

    def __init__(self, max_products: int = 100, progress_callback: Callable = None):
        """
        Inicializa el scraper

        Args:
            max_products: Número máximo de productos a extraer
            progress_callback: Función callback para reportar progreso
        """
        self.max_products = max_products
        self.progress_callback = progress_callback
        self.products: List[Dict] = []
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Añade un delay aleatorio para evitar detección"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def _report_progress(self, current: int, total: int, message: str = ""):
        """Reporta el progreso actual"""
        if self.progress_callback:
            self.progress_callback(current, total, message)
        logger.info(f"Progreso: {current}/{total} - {message}")

    def _extract_product_data(self, product_element) -> Dict:
        """
        Extrae datos de un elemento de producto usando selectores específicos de Vinted

        Args:
            product_element: Elemento HTML del producto

        Returns:
            Diccionario con los datos del producto
        """
        try:
            # Extraer título (data-testid="*-description-title")
            title = "N/A"
            title_elem = product_element.query_selector('p[data-testid*="description-title"]')
            if title_elem:
                title = title_elem.inner_text().strip()

            # Extraer condición/estado (data-testid="*-description-subtitle")
            condition = "N/A"
            condition_elem = product_element.query_selector('p[data-testid*="description-subtitle"]')
            if condition_elem:
                condition = condition_elem.inner_text().strip()

            # Extraer precio (data-testid="*-price-text")
            price = "N/A"
            price_elem = product_element.query_selector('p[data-testid*="price-text"]')
            if price_elem:
                price = price_elem.inner_text().strip()

            # Extraer URL del producto (data-testid="*-overlay-link")
            product_url = ""
            link_elem = product_element.query_selector('a[data-testid*="overlay-link"]')
            if link_elem:
                href = link_elem.get_attribute('href')
                if href:
                    product_url = href if href.startswith('http') else f"https://www.vinted.es{href}"

            # Extraer URL de la imagen (data-testid="*-image--img")
            image_url = "N/A"
            img_elem = product_element.query_selector('img[data-testid*="image--img"]')
            if img_elem:
                src = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
                if src:
                    image_url = src

            # Marca y talla: Vinted no siempre muestra estos datos en el grid
            # Intentar extraer del texto alt de la imagen
            brand = "N/A"
            size = "N/A"

            if img_elem:
                alt_text = img_elem.get_attribute('alt')
                if alt_text:
                    # El alt puede contener info adicional
                    # Ejemplo: "Producto marca, talla M, estado: Nuevo, 10€"
                    parts = alt_text.split(',')
                    if len(parts) > 2:
                        # Intentar extraer talla
                        for part in parts:
                            if 'talla' in part.lower() or 'size' in part.lower():
                                size = part.strip()
                                break

            # Ubicación del vendedor (buscar en metadatos del item)
            location = "N/A"
            location_elem = product_element.query_selector('[class*="location"], [class*="user-location"]')
            if location_elem:
                location = location_elem.inner_text().strip()

            # Si no encontramos ubicación, buscar en el contenedor completo
            if location == "N/A":
                all_text = product_element.inner_text()
                # Buscar patrones comunes de ubicación (ciudades)
                # Esto es opcional y puede mejorarse

            return {
                "title": title,
                "price": price,
                "brand": brand,
                "size": size,
                "condition": condition,
                "product_url": product_url,
                "image_url": image_url,
                "location": location,
                "scraped_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error extrayendo datos del producto: {e}")
            return None

    def _scroll_and_load(self, page: Page, target_products: int) -> None:
        """
        Hace scroll para cargar más productos

        Args:
            page: Página de Playwright
            target_products: Número objetivo de productos a cargar
        """
        last_height = page.evaluate("document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 50

        while len(self.products) < target_products and scroll_attempts < max_scroll_attempts:
            # Scroll hacia abajo
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Esperar a que se carguen nuevos productos
            self._random_delay(2, 4)

            # Calcular nueva altura
            new_height = page.evaluate("document.body.scrollHeight")

            # Extraer productos visibles
            product_elements = page.query_selector_all('.feed-grid__item, [data-testid="item-box"]')

            for elem in product_elements[len(self.products):]:
                if len(self.products) >= target_products:
                    break

                product_data = self._extract_product_data(elem)
                if product_data and product_data not in self.products:
                    self.products.append(product_data)
                    self._report_progress(
                        len(self.products),
                        target_products,
                        f"Extraído: {product_data['title'][:50]}"
                    )

            # Verificar si se llegó al final
            if new_height == last_height:
                scroll_attempts += 1
                logger.info(f"Sin nuevos productos. Intento {scroll_attempts}/{max_scroll_attempts}")
            else:
                scroll_attempts = 0

            last_height = new_height

    def scrape(self, url: str = "https://www.vinted.es/catalog", retries: int = 3) -> List[Dict]:
        """
        Ejecuta el scraping de Vinted

        Args:
            url: URL de la página a scrapear
            retries: Número de reintentos en caso de error

        Returns:
            Lista de productos extraídos
        """
        for attempt in range(retries):
            try:
                logger.info(f"Iniciando scraping (intento {attempt + 1}/{retries})...")
                self._report_progress(0, self.max_products, "Iniciando navegador...")

                with sync_playwright() as p:
                    # Lanzar navegador
                    browser: Browser = p.chromium.launch(headless=False)
                    context = browser.new_context(
                        viewport={'width': 1920, 'height': 1080},
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    )
                    page: Page = context.new_page()

                    # Navegar a la página
                    self._report_progress(0, self.max_products, "Cargando página...")
                    page.goto(url, wait_until='networkidle', timeout=60000)

                    # Esperar a que carguen los productos
                    self._random_delay(3, 5)

                    # Cerrar popups/cookies si existen
                    try:
                        cookie_button = page.query_selector('[data-testid="cookie-accept"], .cookie-notice__button')
                        if cookie_button:
                            cookie_button.click()
                            self._random_delay(1, 2)
                    except:
                        pass

                    # Hacer scroll y extraer productos
                    self._report_progress(0, self.max_products, "Extrayendo productos...")
                    self._scroll_and_load(page, self.max_products)

                    # Cerrar navegador
                    browser.close()

                logger.info(f"Scraping completado. {len(self.products)} productos extraídos.")
                return self.products

            except Exception as e:
                logger.error(f"Error en intento {attempt + 1}: {e}")
                if attempt == retries - 1:
                    logger.error("Todos los reintentos fallaron")
                    raise
                self._random_delay(5, 10)

        return self.products

    def save_to_json(self, filename: str = "productos.json") -> str:
        """
        Guarda los productos en formato JSON

        Args:
            filename: Nombre del archivo

        Returns:
            Ruta del archivo guardado
        """
        filepath = self.data_dir / filename

        data = {
            "metadata": {
                "total_products": len(self.products),
                "scraped_at": datetime.now().isoformat(),
                "source": "vinted.es"
            },
            "products": self.products
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Datos guardados en {filepath}")
        return str(filepath)

    def save_to_csv(self, filename: str = "productos.csv") -> str:
        """
        Guarda los productos en formato CSV

        Args:
            filename: Nombre del archivo

        Returns:
            Ruta del archivo guardado
        """
        if not self.products:
            logger.warning("No hay productos para guardar")
            return ""

        filepath = self.data_dir / filename

        fieldnames = self.products[0].keys()

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.products)

        logger.info(f"Datos guardados en {filepath}")
        return str(filepath)


def main():
    """Función principal para pruebas"""
    def progress_callback(current, total, message):
        print(f"[{current}/{total}] {message}")

    # Importar configuracion de filtros
    try:
        from config_filtros import URL_ROPA_MUJER_VALENCIA
        url_por_defecto = URL_ROPA_MUJER_VALENCIA
        print(f"\nUsando filtro: Ropa de mujer cerca de Valencia")
        print(f"URL: {url_por_defecto}\n")
    except:
        url_por_defecto = "https://www.vinted.es/catalog"
        print(f"\nUsando catalogo general de Vinted.es\n")

    scraper = VintedScraper(max_products=50, progress_callback=progress_callback)

    try:
        products = scraper.scrape(url=url_por_defecto)

        if products:
            scraper.save_to_json()
            scraper.save_to_csv()
            print(f"\n✓ Scraping completado exitosamente")
            print(f"✓ Total de productos: {len(products)}")
        else:
            print("\n✗ No se extrajeron productos")

    except Exception as e:
        print(f"\n✗ Error durante el scraping: {e}")


if __name__ == "__main__":
    main()
