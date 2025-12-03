#!/bin/bash

# Script de setup completo para VPS
# Ejecutar esto DENTRO del VPS después de conectarte con SSH

set -e

echo "================================================"
echo "   VINTED SCRAPER - VPS SETUP COMPLETO"
echo "================================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Actualizar sistema
echo -e "${YELLOW}[1/6] Actualizando sistema...${NC}"
apt update && apt upgrade -y

# 2. Instalar Docker
echo ""
echo -e "${YELLOW}[2/6] Instalando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo -e "${GREEN}✓ Docker instalado${NC}"
else
    echo -e "${GREEN}✓ Docker ya está instalado${NC}"
fi

# 3. Instalar Docker Compose
echo ""
echo -e "${YELLOW}[3/6] Instalando Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose instalado${NC}"
else
    echo -e "${GREEN}✓ Docker Compose ya está instalado${NC}"
fi

# 4. Clonar repositorio
echo ""
echo -e "${YELLOW}[4/6] Clonando repositorio...${NC}"
cd /root
if [ -d "vinted-scraper" ]; then
    echo "Directorio ya existe, actualizando..."
    cd vinted-scraper
    git pull
else
    git clone https://github.com/arlexperalta/vinted-scraper.git
    cd vinted-scraper
fi
echo -e "${GREEN}✓ Repositorio listo${NC}"

# 5. Configurar firewall
echo ""
echo -e "${YELLOW}[5/6] Configurando firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    echo -e "${GREEN}✓ Firewall configurado${NC}"
else
    echo "UFW no disponible, saltando..."
fi

# 6. Desplegar aplicación
echo ""
echo -e "${YELLOW}[6/6] Desplegando aplicación...${NC}"
chmod +x deploy.sh
./deploy.sh

echo ""
echo "================================================"
echo -e "${GREEN}✓✓✓ SETUP COMPLETADO ✓✓✓${NC}"
echo "================================================"
echo ""
echo "Tu aplicación está disponible en:"
echo "  http://157.173.206.22"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs: cd /root/vinted-scraper && docker-compose logs -f"
echo "  - Reiniciar: cd /root/vinted-scraper && docker-compose restart"
echo "  - Estado: cd /root/vinted-scraper && docker-compose ps"
echo ""
