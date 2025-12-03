# 🎯 Guía de Filtros - Valencia, España

Esta guía explica cómo usar el scraper filtrado para buscar solo ropa cerca de Valencia.

## 🚀 Inicio Rápido

### Opción 1: Script Interactivo (RECOMENDADO)

```bash
# Haz doble clic en:
SCRAPER_VALENCIA.bat
```

Este script te mostrará un menú con opciones:
1. Ropa de mujer
2. Ropa de hombre
3. Zapatos de mujer
4. Zapatos de hombre
5. Toda la ropa económica (max 20€)
6. Ropa en muy buen estado
7. Búsqueda personalizada

### Opción 2: Interfaz Web

```bash
# Haz doble clic en:
INICIAR_WEB.bat

# Abre: http://localhost:5000
```

La interfaz web ahora usa automáticamente el filtro de Valencia.

### Opción 3: Línea de Comandos

```bash
cd vinted-scraper
venv\Scripts\activate
python scraper_valencia.py
```

## 📝 Filtros Disponibles

### Por Defecto
- **Ubicación**: Valencia, España
- **Categoría**: Ropa
- **Productos**: Cerca de Valencia

### Categorías Disponibles

#### Ropa
- Ropa de mujer
- Ropa de hombre
- Ropa de niños

#### Zapatos
- Zapatos de mujer
- Zapatos de hombre

#### Otros
- Accesorios

### Filtros Adicionales

#### Por Precio
- Muy barato: 0-10 €
- Barato: 0-20 €
- Medio: 10-50 €
- Caro: 50-200 €
- Sin límite

#### Por Estado
- Nuevo
- Muy bueno
- Bueno
- Satisfactorio

## 🔧 Crear URLs Personalizadas

### Método 1: Usando config_filtros.py

```python
from config_filtros import construir_url_vinted

# Ropa de mujer en Valencia, máximo 30€
url = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    precio_max=30
)

print(url)
```

### Método 2: Búsqueda por Palabra Clave

```python
from config_filtros import construir_url_vinted

# Buscar "vestido" en Valencia
url = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    busqueda="vestido",
    precio_max=50
)
```

### Método 3: Filtro por Estado

```python
from config_filtros import construir_url_vinted

# Solo ropa nueva o en muy buen estado
url = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    estado="muy_bueno"
)
```

## 📊 Ejemplos de Uso

### Ejemplo 1: Ropa de Mujer Económica

```python
from scraper import VintedScraper
from config_filtros import construir_url_vinted

url = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    precio_max=15
)

scraper = VintedScraper(max_products=30)
productos = scraper.scrape(url=url)
scraper.save_to_json()
```

### Ejemplo 2: Zapatos de Hombre Nuevos

```python
from scraper import VintedScraper
from config_filtros import construir_url_vinted

url = construir_url_vinted(
    pais="es",
    categoria="zapatos_hombre",
    ubicacion="valencia",
    estado="nuevo",
    precio_max=50
)

scraper = VintedScraper(max_products=20)
productos = scraper.scrape(url=url)
scraper.save_to_json()
```

### Ejemplo 3: Búsqueda de Marca Específica

```python
from scraper import VintedScraper
from config_filtros import construir_url_vinted

url = construir_url_vinted(
    pais="es",
    categoria="toda_ropa",
    ubicacion="valencia",
    busqueda="nike"  # Buscar Nike
)

scraper = VintedScraper(max_products=25)
productos = scraper.scrape(url=url)
scraper.save_to_json()
```

## 🌍 Cambiar de Ciudad

Si quieres buscar en otra ciudad de España, edita `config_filtros.py`:

```python
UBICACIONES = {
    "valencia": {
        "ciudad": "Valencia",
        "ciudad_id": "21898",
    },
    "madrid": {
        "ciudad": "Madrid",
        "ciudad_id": "21892",
    },
    "barcelona": {
        "ciudad": "Barcelona",
        "ciudad_id": "21899",
    },
    # Añade tu ciudad aquí
    "alicante": {
        "ciudad": "Alicante",
        "ciudad_id": "XXXXX",  # Encuentra el ID
    }
}
```

**Nota**: Para encontrar el ID de tu ciudad, inspecciona la URL de Vinted cuando filtres manualmente.

## 🎨 Estructura de URLs de Vinted

Las URLs de Vinted siguen este formato:

```
https://www.vinted.es/catalog?catalog[]=CATEGORIA&city_ids[]=CIUDAD&price_to=MAX&status[]=ESTADO
```

Ejemplos reales:

```
# Ropa de mujer en Valencia
https://www.vinted.es/catalog?catalog[]=1904

# Ropa barata (max 20€)
https://www.vinted.es/catalog?catalog[]=1904&price_to=20

# Ropa en muy buen estado
https://www.vinted.es/catalog?catalog[]=1904&status[]=muy+bueno

# Buscar "vestido rojo"
https://www.vinted.es/catalog?search_text=vestido+rojo
```

## ⚙️ Configuración Avanzada

### Ejecutar Desde Python Directamente

```python
from scraper import VintedScraper

# URL completa con todos los filtros
url = "https://www.vinted.es/catalog?catalog[]=1904&price_to=30&status[]=muy+bueno"

scraper = VintedScraper(max_products=50)
productos = scraper.scrape(url=url)

# Guardar
scraper.save_to_json()
scraper.save_to_csv()
```

### Múltiples Búsquedas

```python
from scraper import VintedScraper
from config_filtros import construir_url_vinted

categorias = ["ropa_mujer", "zapatos_mujer", "accesorios"]

for categoria in categorias:
    url = construir_url_vinted(
        pais="es",
        categoria=categoria,
        ubicacion="valencia",
        precio_max=25
    )

    scraper = VintedScraper(max_products=20)
    productos = scraper.scrape(url=url)
    scraper.save_to_json(f"productos_{categoria}.json")

    print(f"{categoria}: {len(productos)} productos encontrados")
```

## 📌 Notas Importantes

1. **Ubicación**: Vinted puede no siempre respetar el filtro de ciudad exacto, pero priorizará vendedores cercanos.

2. **Categorías**: Los IDs de categorías pueden cambiar. Si no funcionan, inspecciona manualmente Vinted.

3. **Límites**: No hagas scraping excesivo. Respeta los servidores de Vinted.

4. **Datos**: Marca, talla y ubicación exacta solo están disponibles en la página individual del producto, no en el grid.

## 🆘 Solución de Problemas

### No encuentra productos
- Verifica que los filtros no sean demasiado restrictivos
- Prueba sin filtro de precio primero
- Asegúrate de tener conexión a Internet

### Error en la URL
- Verifica que los IDs de categoría/ciudad sean correctos
- Prueba primero con el catálogo general: `https://www.vinted.es/catalog`

### Productos duplicados
- Normal en el grid de Vinted
- El scraper intenta evitarlos pero puede haber algunos

## 📞 Ayuda

Para más información:
- README.md (documentación general)
- TIPS.md (trucos avanzados)
- example_usage.py (ejemplos de código)

¡Disfruta buscando ropa en Valencia! 🎉
