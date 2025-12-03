"""
Configuracion de filtros para Vinted Scraper
Define URLs pre-configuradas con filtros especificos
"""

# URLs base de Vinted por pais
VINTED_BASE_URLS = {
    "es": "https://www.vinted.es/catalog",
    "fr": "https://www.vinted.fr/catalog",
    "it": "https://www.vinted.it/catalog",
    "de": "https://www.vinted.de/catalog"
}

# Categorias principales de ropa en Vinted.es
# Estos IDs pueden variar, se recomienda verificarlos en Vinted
CATEGORIAS = {
    "ropa_mujer": "catalog[]=1904",  # Mujer > Ropa
    "ropa_hombre": "catalog[]=1193",  # Hombre > Ropa
    "ropa_ninos": "catalog[]=1358",   # Niños
    "zapatos_mujer": "catalog[]=16",  # Mujer > Zapatos
    "zapatos_hombre": "catalog[]=12", # Hombre > Zapatos
    "accesorios": "catalog[]=1191",   # Accesorios
    "toda_ropa": ""  # Sin filtro de categoria
}

# Ubicaciones principales en España
# Valencia y alrededores
UBICACIONES = {
    "valencia": {
        "ciudad": "Valencia",
        "ciudad_id": "21898",  # ID aproximado, puede variar
    },
    "madrid": {
        "ciudad": "Madrid",
        "ciudad_id": "21892",
    },
    "barcelona": {
        "ciudad": "Barcelona",
        "ciudad_id": "21899",
    },
    "toda_espana": {
        "ciudad": "España",
        "ciudad_id": None,
    }
}

# Rangos de precio comunes
RANGOS_PRECIO = {
    "muy_barato": {"min": 0, "max": 10},
    "barato": {"min": 0, "max": 20},
    "medio": {"min": 10, "max": 50},
    "caro": {"min": 50, "max": 200},
    "sin_limite": {"min": None, "max": None}
}

# Estados/Condiciones
ESTADOS = {
    "nuevo": "nuevo",
    "muy_bueno": "muy+bueno",
    "bueno": "bueno",
    "satisfactorio": "satisfactorio",
    "todos": None
}


def construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia",
    precio_min=None,
    precio_max=None,
    busqueda=None,
    estado=None
):
    """
    Construye una URL de Vinted con los filtros especificados

    Args:
        pais: Codigo del pais (es, fr, it, de)
        categoria: Categoria de ropa (ver CATEGORIAS)
        ubicacion: Ciudad o region (ver UBICACIONES)
        precio_min: Precio minimo en euros
        precio_max: Precio maximo en euros
        busqueda: Termino de busqueda (ej: "nike", "vestido rojo")
        estado: Estado del producto (ver ESTADOS)

    Returns:
        URL completa con filtros
    """
    # URL base
    url = VINTED_BASE_URLS.get(pais, VINTED_BASE_URLS["es"])

    parametros = []

    # Agregar categoria
    if categoria in CATEGORIAS and CATEGORIAS[categoria]:
        parametros.append(CATEGORIAS[categoria])

    # Agregar ubicacion
    if ubicacion in UBICACIONES:
        loc = UBICACIONES[ubicacion]
        if loc["ciudad_id"]:
            parametros.append(f"city_ids[]={loc['ciudad_id']}")
        # Para búsqueda por texto de ciudad
        if busqueda is None and ubicacion != "toda_espana":
            # Podemos agregar la ciudad como filtro de texto
            pass

    # Agregar busqueda de texto
    if busqueda:
        parametros.append(f"search_text={busqueda.replace(' ', '+')}")

    # Agregar rango de precio
    if precio_min is not None:
        parametros.append(f"price_from={precio_min}")
    if precio_max is not None:
        parametros.append(f"price_to={precio_max}")

    # Agregar estado
    if estado and estado in ESTADOS and ESTADOS[estado]:
        parametros.append(f"status[]={ESTADOS[estado]}")

    # Construir URL final
    if parametros:
        url += "?" + "&".join(parametros)

    return url


# URLs PRE-CONFIGURADAS COMUNES

# Ropa de mujer en Valencia
URL_ROPA_MUJER_VALENCIA = construir_url_vinted(
    pais="es",
    categoria="ropa_mujer",
    ubicacion="valencia"
)

# Ropa de hombre en Valencia
URL_ROPA_HOMBRE_VALENCIA = construir_url_vinted(
    pais="es",
    categoria="ropa_hombre",
    ubicacion="valencia"
)

# Toda la ropa cerca de Valencia, económica
URL_ROPA_ECONOMICA_VALENCIA = construir_url_vinted(
    pais="es",
    categoria="toda_ropa",
    ubicacion="valencia",
    precio_max=20
)

# Zapatos de mujer en Valencia
URL_ZAPATOS_MUJER_VALENCIA = construir_url_vinted(
    pais="es",
    categoria="zapatos_mujer",
    ubicacion="valencia"
)

# Ropa en buen estado, Valencia
URL_ROPA_BUEN_ESTADO_VALENCIA = construir_url_vinted(
    pais="es",
    categoria="toda_ropa",
    ubicacion="valencia",
    estado="muy_bueno"
)

# EJEMPLOS DE USO
URLS_EJEMPLO = {
    "ropa_mujer_valencia": URL_ROPA_MUJER_VALENCIA,
    "ropa_hombre_valencia": URL_ROPA_HOMBRE_VALENCIA,
    "ropa_economica_valencia": URL_ROPA_ECONOMICA_VALENCIA,
    "zapatos_mujer_valencia": URL_ZAPATOS_MUJER_VALENCIA,
    "ropa_buen_estado_valencia": URL_ROPA_BUEN_ESTADO_VALENCIA,
}


def mostrar_urls_disponibles():
    """Muestra todas las URLs pre-configuradas"""
    print("\n" + "="*60)
    print("URLs PRE-CONFIGURADAS PARA VALENCIA")
    print("="*60)

    for nombre, url in URLS_EJEMPLO.items():
        print(f"\n{nombre}:")
        print(f"  {url}")

    print("\n" + "="*60)


if __name__ == "__main__":
    mostrar_urls_disponibles()

    # Ejemplo de URL personalizada
    print("\nEJEMPLO - Crear URL personalizada:")
    print("="*60)

    url_custom = construir_url_vinted(
        pais="es",
        categoria="ropa_mujer",
        ubicacion="valencia",
        busqueda="vestido",
        precio_max=30
    )

    print(f"\nBuscar 'vestido' en Valencia, max 30€:")
    print(f"  {url_custom}")
    print("="*60)
