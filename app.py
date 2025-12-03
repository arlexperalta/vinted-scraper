"""
Flask Web Application para Vinted Scraper
Proporciona interfaz web para visualizar y filtrar productos
"""

from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import json
import threading
from pathlib import Path
from datetime import datetime
import logging
from scraper import VintedScraper

# Configuración
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado global del scraping
scraping_state = {
    "is_running": False,
    "progress": 0,
    "total": 0,
    "message": "",
    "last_update": None
}

DATA_FILE = Path("data/productos.json")


def load_products():
    """Carga productos desde el archivo JSON"""
    if not DATA_FILE.exists():
        return {"metadata": {"total_products": 0, "scraped_at": None}, "products": []}

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error cargando productos: {e}")
        return {"metadata": {"total_products": 0, "scraped_at": None}, "products": []}


def progress_callback(current, total, message):
    """Callback para actualizar el progreso del scraping"""
    global scraping_state
    scraping_state.update({
        "progress": current,
        "total": total,
        "message": message,
        "last_update": datetime.now().isoformat()
    })


def run_scraper(max_products, url=None):
    """Ejecuta el scraper en un thread separado"""
    global scraping_state

    try:
        scraping_state["is_running"] = True
        scraping_state["message"] = "Iniciando scraper..."

        # Si no se proporciona URL, usar la de Valencia por defecto
        if url is None:
            try:
                from config_filtros import URL_ROPA_MUJER_VALENCIA
                url = URL_ROPA_MUJER_VALENCIA
                logger.info(f"Usando filtro de Valencia: {url}")
            except:
                url = "https://www.vinted.es/catalog"
                logger.info("Usando catalogo general")

        scraper = VintedScraper(max_products=max_products, progress_callback=progress_callback)
        products = scraper.scrape(url=url)

        if products:
            scraper.save_to_json()
            scraper.save_to_csv()
            scraping_state["message"] = f"Completado: {len(products)} productos"
        else:
            scraping_state["message"] = "No se encontraron productos"

    except Exception as e:
        logger.error(f"Error en scraping: {e}")
        scraping_state["message"] = f"Error: {str(e)}"

    finally:
        scraping_state["is_running"] = False


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Obtiene la lista de productos con filtros opcionales

    Query params:
        - search: Búsqueda de texto en título/marca
        - min_price: Precio mínimo
        - max_price: Precio máximo
        - brand: Filtrar por marca
        - size: Filtrar por talla
        - condition: Filtrar por estado
        - sort_by: Ordenar por (price, brand, date)
        - sort_order: asc o desc
    """
    data = load_products()
    products = data.get("products", [])

    # Aplicar filtros
    search = request.args.get('search', '').lower()
    if search:
        products = [p for p in products if
                   search in p.get('title', '').lower() or
                   search in p.get('brand', '').lower()]

    # Filtro de marca
    brand = request.args.get('brand', '').lower()
    if brand and brand != 'todas':
        products = [p for p in products if brand in p.get('brand', '').lower()]

    # Filtro de talla
    size = request.args.get('size', '').lower()
    if size and size != 'todas':
        products = [p for p in products if size in p.get('size', '').lower()]

    # Filtro de estado
    condition = request.args.get('condition', '').lower()
    if condition and condition != 'todos':
        products = [p for p in products if condition in p.get('condition', '').lower()]

    # Filtro de precio
    try:
        min_price = float(request.args.get('min_price', 0))
        max_price = float(request.args.get('max_price', float('inf')))

        filtered_products = []
        for p in products:
            price_str = p.get('price', '0').replace('€', '').replace(',', '.').strip()
            try:
                price = float(price_str.split()[0])
                if min_price <= price <= max_price:
                    filtered_products.append(p)
            except:
                filtered_products.append(p)  # Incluir si no se puede parsear

        products = filtered_products

    except ValueError:
        pass

    # Ordenamiento
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')

    if sort_by == 'price':
        products.sort(
            key=lambda x: float(x.get('price', '0').replace('€', '').replace(',', '.').strip().split()[0] or 0),
            reverse=(sort_order == 'desc')
        )
    elif sort_by == 'brand':
        products.sort(key=lambda x: x.get('brand', ''), reverse=(sort_order == 'desc'))
    elif sort_by == 'date':
        products.sort(key=lambda x: x.get('scraped_at', ''), reverse=(sort_order == 'desc'))

    return jsonify({
        "products": products,
        "metadata": data.get("metadata", {}),
        "total": len(products)
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas de los productos"""
    data = load_products()
    products = data.get("products", [])

    if not products:
        return jsonify({
            "total_products": 0,
            "brands": [],
            "sizes": [],
            "conditions": [],
            "price_range": {"min": 0, "max": 0}
        })

    # Extraer valores únicos
    brands = sorted(list(set(p.get('brand', 'N/A') for p in products if p.get('brand', 'N/A') != 'N/A')))
    sizes = sorted(list(set(p.get('size', 'N/A') for p in products if p.get('size', 'N/A') != 'N/A')))
    conditions = sorted(list(set(p.get('condition', 'N/A') for p in products if p.get('condition', 'N/A') != 'N/A')))

    # Calcular rango de precios
    prices = []
    for p in products:
        try:
            price_str = p.get('price', '0').replace('€', '').replace(',', '.').strip()
            price = float(price_str.split()[0])
            prices.append(price)
        except:
            pass

    price_range = {
        "min": min(prices) if prices else 0,
        "max": max(prices) if prices else 0
    }

    return jsonify({
        "total_products": len(products),
        "brands": brands,
        "sizes": sizes,
        "conditions": conditions,
        "price_range": price_range,
        "last_update": data.get("metadata", {}).get("scraped_at")
    })


@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    """Inicia el proceso de scraping"""
    global scraping_state

    if scraping_state["is_running"]:
        return jsonify({
            "success": False,
            "message": "El scraping ya está en ejecución"
        }), 400

    max_products = request.json.get('max_products', 100)

    # Iniciar scraping en thread separado
    thread = threading.Thread(target=run_scraper, args=(max_products,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "success": True,
        "message": "Scraping iniciado"
    })


@app.route('/api/scrape/status', methods=['GET'])
def get_scraping_status():
    """Obtiene el estado actual del scraping"""
    return jsonify(scraping_state)


@app.route('/api/scrape/progress')
def scrape_progress():
    """
    Server-Sent Events para progreso en tiempo real
    """
    def generate():
        while scraping_state["is_running"]:
            yield f"data: {json.dumps(scraping_state)}\n\n"
            threading.Event().wait(1)

        # Enviar último estado
        yield f"data: {json.dumps(scraping_state)}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    # Crear directorio de datos si no existe
    Path("data").mkdir(exist_ok=True)

    # Detectar si estamos en producción
    import os
    is_production = os.getenv('FLASK_ENV') == 'production'
    debug_mode = not is_production

    print("\n" + "="*60)
    print("🚀 VINTED SCRAPER - Servidor Web")
    print("="*60)
    print(f"📍 Accede a: http://localhost:5000")
    print(f"📊 API Base: http://localhost:5000/api")
    print(f"🔧 Modo: {'Producción' if is_production else 'Desarrollo'}")
    print("="*60 + "\n")

    app.run(debug=debug_mode, host='0.0.0.0', port=5000, threaded=True)
