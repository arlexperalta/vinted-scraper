# 🛍️ Vinted Scraper

Un scraper completo de Vinted.es con interfaz web interactiva. Extrae productos, almacena datos en JSON/CSV y proporciona una interfaz web con filtros avanzados.

## ✨ Características

### 🔍 Scraping
- **Playwright**: Scraping robusto con navegador real
- **Scroll automático**: Carga entre 50-100 productos (configurable)
- **Delays aleatorios**: Evita detección
- **Extracción completa**: Título, precio, marca, talla, estado, URLs, ubicación
- **Reintentos automáticos**: Manejo de errores robusto

### 💾 Almacenamiento
- **JSON**: Formato estructurado con metadata
- **CSV**: Exportación para Excel/análisis
- **Persistencia**: Datos guardados en `/data`

### 🌐 Interfaz Web
- **Dashboard moderno**: Diseño responsive y limpio
- **Tabla interactiva**: Click para abrir productos en nueva pestaña
- **Filtros múltiples**:
  - 🔍 Búsqueda de texto (título/marca)
  - 💰 Rango de precios
  - 🏷️ Marca, talla, estado
  - 📊 Ordenamiento (precio, marca, fecha)
- **Barra de progreso**: Actualización en tiempo real
- **Estadísticas**: Total productos, última actualización
- **Botón actualizar**: Re-scrape desde la interfaz

## 📁 Estructura del Proyecto

```
vinted-scraper/
├── scraper.py           # Lógica de scraping con Playwright
├── app.py              # Servidor Flask con API REST
├── requirements.txt    # Dependencias Python
├── README.md          # Documentación
├── templates/
│   └── index.html     # Interfaz web
├── data/
│   ├── productos.json # Datos en JSON
│   └── productos.csv  # Datos en CSV
└── static/            # Archivos estáticos (si es necesario)
```

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el proyecto

```bash
cd vinted-scraper
```

### Paso 2: Crear entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar navegadores de Playwright

```bash
playwright install chromium
```

## 🎯 Uso

### Opción 1: Usar la Interfaz Web (Recomendado)

1. **Iniciar el servidor Flask:**

```bash
python app.py
```

2. **Abrir el navegador:**

Visita: `http://localhost:5000`

3. **Usar la interfaz:**
   - Haz clic en "🔄 Actualizar Datos"
   - Ingresa el número de productos a extraer (ej: 100)
   - Espera a que termine el scraping
   - Usa los filtros para explorar los productos

### Opción 2: Usar el Scraper Directamente

```bash
python scraper.py
```

Esto ejecutará el scraper y guardará los datos en `/data`.

### Opción 3: Importar como módulo

```python
from scraper import VintedScraper

def mi_callback(current, total, message):
    print(f"[{current}/{total}] {message}")

scraper = VintedScraper(max_products=100, progress_callback=mi_callback)
products = scraper.scrape()

scraper.save_to_json()
scraper.save_to_csv()

print(f"Extraídos {len(products)} productos")
```

## 🎨 Funcionalidades de la Interfaz Web

### Filtros Disponibles
- **Búsqueda**: Busca en títulos y marcas
- **Precio**: Define rango mínimo y máximo
- **Marca**: Filtra por marca específica
- **Talla**: Filtra por talla
- **Estado**: Nuevo, como nuevo, usado, etc.

### Ordenamiento
- Por **precio** (ascendente/descendente)
- Por **marca** (alfabético)
- Por **fecha** (más recientes primero)

### Estadísticas
- Total de productos scrapeados
- Última actualización
- Productos visibles (después de filtros)

## 🛠️ API Endpoints

### GET `/api/products`
Obtiene productos con filtros opcionales.

**Query params:**
- `search`: Texto a buscar
- `min_price`: Precio mínimo
- `max_price`: Precio máximo
- `brand`: Marca
- `size`: Talla
- `condition`: Estado
- `sort_by`: Campo de ordenamiento
- `sort_order`: `asc` o `desc`

**Ejemplo:**
```bash
curl "http://localhost:5000/api/products?brand=Zara&min_price=10&max_price=50"
```

### GET `/api/stats`
Obtiene estadísticas generales.

**Respuesta:**
```json
{
  "total_products": 100,
  "brands": ["Zara", "H&M", ...],
  "sizes": ["S", "M", "L", ...],
  "conditions": ["Nuevo", "Como nuevo", ...],
  "price_range": {"min": 5, "max": 200},
  "last_update": "2025-01-19T10:30:00"
}
```

### POST `/api/scrape`
Inicia el proceso de scraping.

**Body:**
```json
{
  "max_products": 100
}
```

### GET `/api/scrape/status`
Obtiene el estado actual del scraping.

### GET `/api/scrape/progress`
Server-Sent Events para progreso en tiempo real.

## 📝 Configuración Avanzada

### Cambiar URL de scraping

Edita `scraper.py`:

```python
scraper.scrape(url="https://www.vinted.es/catalog?search_text=zapatos")
```

### Ajustar delays

Edita `scraper.py`, método `_random_delay`:

```python
self._random_delay(min_seconds=2.0, max_seconds=5.0)
```

### Cambiar puerto del servidor

Edita `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## ⚠️ Consideraciones Importantes

### Términos de Servicio
- Este scraper es solo para **uso educativo**
- Revisa los términos de servicio de Vinted antes de usar
- No hagas scraping excesivo que pueda sobrecargar los servidores

### Rate Limiting
- El scraper incluye delays aleatorios
- No ejecutes múltiples instancias simultáneas
- Respeta los límites de la plataforma

### Datos Personales
- El scraper solo extrae información pública
- No extrae datos de usuarios ni información privada

## 🐛 Solución de Problemas

### Error: "playwright not found"
```bash
playwright install chromium
```

### Error: "Port 5000 already in use"
Cambia el puerto en `app.py` o cierra la aplicación que usa el puerto 5000.

### No se cargan productos
- Verifica tu conexión a Internet
- Vinted puede estar bloqueando requests (cambia user-agent)
- Aumenta los delays en `scraper.py`

### El navegador no se abre
Asegúrate de que Playwright está instalado correctamente:
```bash
playwright install --with-deps chromium
```

## 📊 Formato de Datos

### JSON
```json
{
  "metadata": {
    "total_products": 100,
    "scraped_at": "2025-01-19T10:30:00",
    "source": "vinted.es"
  },
  "products": [
    {
      "title": "Zapatillas Nike",
      "price": "45.00 €",
      "brand": "Nike",
      "size": "42",
      "condition": "Como nuevo",
      "product_url": "https://www.vinted.es/items/...",
      "image_url": "https://images.vinted.net/...",
      "location": "Madrid",
      "scraped_at": "2025-01-19T10:30:00"
    }
  ]
}
```

### CSV
```csv
title,price,brand,size,condition,product_url,image_url,location,scraped_at
Zapatillas Nike,45.00 €,Nike,42,Como nuevo,https://...,https://...,Madrid,2025-01-19T10:30:00
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado con ❤️ para la comunidad de Python y web scraping.

## 🚀 Deployment en VPS

¿Quieres poner tu aplicación online? Tenemos todo preparado:

### Guías disponibles:
- **QUICK-START-VPS.md**: Guía rápida de 5 minutos
- **DEPLOYMENT.md**: Guía completa paso a paso

### Lo que incluye:
- 🐳 Dockerfile y docker-compose.yml
- 🌐 Configuración de Nginx como proxy reverso
- 📜 Scripts automatizados de deployment
- 🔒 Instrucciones para SSL/HTTPS
- 💾 Scripts de backup

### Despliegue rápido:
```bash
# En tu VPS
git clone https://github.com/TU-USUARIO/vinted-scraper.git
cd vinted-scraper
chmod +x deploy.sh
./deploy.sh
```

Tu app estará disponible en: `http://TU_IP_DEL_VPS`

## 🙏 Agradecimientos

- [Playwright](https://playwright.dev/) - Framework de automatización
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Vinted](https://www.vinted.es/) - Fuente de datos
- [Docker](https://www.docker.com/) - Containerización
- [Nginx](https://nginx.org/) - Servidor web

---

**Nota:** Este proyecto es solo para fines educativos. Asegúrate de cumplir con los términos de servicio de Vinted y las leyes aplicables sobre web scraping.
