# 💡 Tips y Mejoras Avanzadas

## 🚀 Optimizaciones

### 1. Scraping Más Rápido
Si necesitas extraer datos más rápidamente, puedes reducir los delays en `scraper.py`:

```python
# Busca esta línea
self._random_delay(2, 4)

# Cámbiala a:
self._random_delay(1, 2)
```

**⚠️ Advertencia:** Delays muy cortos pueden resultar en bloqueos.

### 2. Modo Headless
Para scraping más eficiente sin abrir el navegador, edita `scraper.py`:

```python
# Busca esta línea
browser: Browser = p.chromium.launch(headless=False)

# Cámbiala a:
browser: Browser = p.chromium.launch(headless=True)
```

### 3. Scraping Paralelo
Para extraer de múltiples categorías simultáneamente:

```python
from concurrent.futures import ThreadPoolExecutor
from scraper import VintedScraper

def scrape_category(url, name):
    scraper = VintedScraper(max_products=50)
    products = scraper.scrape(url=url)
    scraper.save_to_json(f"productos_{name}.json")
    return len(products)

urls = {
    "zapatos": "https://www.vinted.es/catalog?search_text=zapatos",
    "ropa": "https://www.vinted.es/catalog?search_text=ropa",
    "bolsos": "https://www.vinted.es/catalog?search_text=bolsos"
}

with ThreadPoolExecutor(max_workers=3) as executor:
    results = {name: executor.submit(scrape_category, url, name)
               for name, url in urls.items()}

    for name, future in results.items():
        print(f"{name}: {future.result()} productos")
```

## 🎯 Búsquedas Específicas

### Buscar por Término
```python
url = "https://www.vinted.es/catalog?search_text=nike+zapatillas"
scraper.scrape(url=url)
```

### Buscar en Categoría
```python
# Mujer > Ropa
url = "https://www.vinted.es/catalog?catalog[]=1904"
scraper.scrape(url=url)
```

### Filtros Avanzados en URL
```python
# Precio entre 10-50€, talla M
url = "https://www.vinted.es/catalog?price_from=10&price_to=50&size_ids[]=206"
scraper.scrape(url=url)
```

## 🔧 Mejoras Técnicas

### 1. Base de Datos SQLite
Para mejor rendimiento con muchos productos:

```python
import sqlite3

def create_database():
    conn = sqlite3.connect('data/productos.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            brand TEXT,
            size TEXT,
            condition TEXT,
            product_url TEXT UNIQUE,
            image_url TEXT,
            location TEXT,
            scraped_at TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_to_database(products):
    conn = sqlite3.connect('data/productos.db')
    cursor = conn.cursor()

    for product in products:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO productos
                (title, price, brand, size, condition, product_url, image_url, location, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product['title'],
                float(product['price'].replace('€', '').replace(',', '.').strip().split()[0] or 0),
                product['brand'],
                product['size'],
                product['condition'],
                product['product_url'],
                product['image_url'],
                product['location'],
                product['scraped_at']
            ))
        except:
            pass

    conn.commit()
    conn.close()
```

### 2. Sistema de Notificaciones
Notificación cuando aparecen productos nuevos:

```python
def check_new_products(old_urls, new_products):
    new_items = [p for p in new_products if p['product_url'] not in old_urls]

    if new_items:
        print(f"🔔 {len(new_items)} productos nuevos encontrados!")
        for item in new_items[:5]:  # Mostrar primeros 5
            print(f"  - {item['title']} - {item['price']}")
```

### 3. Scraping Programado
Ejecutar automáticamente cada hora:

```python
import schedule
import time

def job():
    print("Ejecutando scraping...")
    scraper = VintedScraper(max_products=50)
    scraper.scrape()
    scraper.save_to_json()
    print("✓ Scraping completado")

# Cada hora
schedule.every(1).hours.do(job)

# Ejecutar
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 4. Exportar a Excel
Para análisis más avanzados:

```python
import pandas as pd

def export_to_excel(json_file, excel_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data['products'])

    # Crear Excel con formato
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Productos', index=False)

        # Ajustar anchos de columna
        worksheet = writer.sheets['Productos']
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

export_to_excel('data/productos.json', 'data/productos.xlsx')
```

## 📊 Análisis de Datos Avanzado

### Dashboard con Plotly
```python
import plotly.express as px
import pandas as pd

def create_dashboard(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data['products'])

    # Gráfico de precios por marca
    fig = px.box(df, x='brand', y='price', title='Distribución de Precios por Marca')
    fig.show()

    # Gráfico de productos por estado
    condition_counts = df['condition'].value_counts()
    fig = px.pie(values=condition_counts.values, names=condition_counts.index,
                 title='Distribución por Estado')
    fig.show()
```

### Detección de Ofertas
```python
def find_deals(products, percentile=25):
    """Encuentra productos con precios por debajo del percentil dado"""
    prices = []
    for p in products:
        try:
            price = float(p['price'].replace('€', '').replace(',', '.').strip().split()[0])
            prices.append(price)
        except:
            pass

    threshold = np.percentile(prices, percentile)

    deals = [p for p in products
             if float(p['price'].replace('€', '').replace(',', '.').strip().split()[0] or 999) <= threshold]

    print(f"🎉 {len(deals)} ofertas encontradas (precio <= {threshold:.2f}€)")
    return deals
```

## 🛡️ Manejo de Errores Avanzado

### Retry con Backoff Exponencial
```python
import time

def scrape_with_retry(max_retries=5):
    for attempt in range(max_retries):
        try:
            scraper = VintedScraper(max_products=50)
            products = scraper.scrape()
            return products
        except Exception as e:
            wait_time = 2 ** attempt  # Backoff exponencial
            print(f"Error en intento {attempt + 1}, esperando {wait_time}s...")
            time.sleep(wait_time)

            if attempt == max_retries - 1:
                raise
```

### Logging Detallado
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
```

## 🔒 Seguridad y Privacidad

### 1. User Agent Rotación
```python
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...'
]

user_agent = random.choice(USER_AGENTS)
context = browser.new_context(user_agent=user_agent)
```

### 2. Proxy Support
```python
context = browser.new_context(
    proxy={
        "server": "http://proxy-server:port",
        "username": "user",
        "password": "pass"
    }
)
```

## 📱 Integración con APIs

### Webhook para Notificaciones
```python
import requests

def send_webhook(products_count):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

    data = {
        "text": f"🛍️ Scraping completado: {products_count} productos extraídos"
    }

    requests.post(webhook_url, json=data)
```

## 🎨 Mejoras de Interfaz

### 1. Agregar Gráficos
Añade Chart.js al `index.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="priceChart"></canvas>

<script>
const ctx = document.getElementById('priceChart');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: brands,
        datasets: [{
            label: 'Productos por Marca',
            data: counts
        }]
    }
});
</script>
```

### 2. Modo Oscuro
Añade toggle de tema oscuro en la interfaz.

### 3. Exportar Resultados
Botón para exportar productos filtrados a CSV desde la interfaz.

## 🔄 Mantenimiento

### Script de Limpieza
```python
import os
from datetime import datetime, timedelta

def clean_old_data(days=7):
    """Elimina datos más antiguos que X días"""
    data_dir = Path("data")
    cutoff = datetime.now() - timedelta(days=days)

    for file in data_dir.glob("productos_*.json"):
        if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
            file.unlink()
            print(f"Eliminado: {file.name}")
```

## 📝 Notas Finales

- Siempre respeta los términos de servicio de Vinted
- No hagas scraping excesivo (máximo 1-2 veces por hora)
- Monitorea el uso de memoria y CPU
- Mantén actualizado Playwright: `pip install --upgrade playwright`
- Revisa los logs regularmente para detectar problemas

---

¿Más preguntas? Consulta la documentación oficial de [Playwright](https://playwright.dev/python/) y [Flask](https://flask.palletsprojects.com/).
