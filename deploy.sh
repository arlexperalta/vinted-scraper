#!/bin/bash

# Script de deployment para VPS
# Este script debe ejecutarse en el VPS

set -e  # Exit on error

echo "================================================"
echo "   VINTED SCRAPER - DEPLOYMENT SCRIPT"
echo "================================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker no está instalado${NC}"
    echo "Instala Docker primero: https://docs.docker.com/engine/install/"
    exit 1
fi

# Verificar que Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose no está instalado${NC}"
    echo "Instala Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker y Docker Compose encontrados${NC}"
echo ""

# Detener contenedores existentes
echo "Deteniendo contenedores existentes..."
docker-compose down 2>/dev/null || true

# Limpiar imágenes antiguas (opcional)
echo "¿Deseas limpiar imágenes Docker antiguas? (s/n)"
read -r clean_images
if [ "$clean_images" = "s" ]; then
    echo "Limpiando imágenes antiguas..."
    docker system prune -f
fi

# Construir imágenes
echo ""
echo "Construyendo imágenes Docker..."
docker-compose build --no-cache

# Crear directorios necesarios
echo ""
echo "Creando directorios..."
mkdir -p data
mkdir -p nginx/ssl

# Iniciar servicios
echo ""
echo "Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo ""
echo "Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado
echo ""
echo "Estado de los contenedores:"
docker-compose ps

# Mostrar logs
echo ""
echo "Últimas líneas de logs:"
docker-compose logs --tail=20

echo ""
echo "================================================"
echo -e "${GREEN}✓ Deployment completado!${NC}"
echo "================================================"
echo ""
echo "Accede a tu aplicación en:"
echo "  http://TU_IP_DEL_VPS"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Reiniciar: docker-compose restart"
echo "  - Detener: docker-compose down"
echo "  - Ver estado: docker-compose ps"
echo ""
