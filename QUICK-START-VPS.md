# Quick Start - Despliegue en VPS

Guía rápida de 5 minutos para poner tu app online.

## En tu PC Local

### 1. Subir proyecto a GitHub

```bash
# Crear repo en GitHub primero, luego:
git init
git add .
git commit -m "Vinted scraper ready for deployment"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/vinted-scraper.git
git push -u origin main
```

## En tu VPS

### 2. Instalar Docker (si no lo tienes)

```bash
# Conectarse al VPS
ssh usuario@tu-ip-del-vps

# Instalación rápida de Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Clonar y desplegar

```bash
# Clonar proyecto
git clone https://github.com/TU-USUARIO/vinted-scraper.git
cd vinted-scraper

# Abrir puertos
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Desplegar
chmod +x deploy.sh
./deploy.sh
```

### 4. Acceder

Abre tu navegador: `http://TU_IP_DEL_VPS`

## Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Detener
docker-compose down

# Actualizar app
git pull && docker-compose up -d --build
```

## Troubleshooting

**App no funciona?**
```bash
# Verificar contenedores
docker-compose ps

# Ver logs de errores
docker-compose logs web
docker-compose logs nginx
```

**Sin memoria?**
```bash
# Añadir 2GB de swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Puerto 80 ocupado?**
```bash
sudo systemctl stop apache2
docker-compose restart nginx
```

---

**Para más detalles:** Lee DEPLOYMENT.md

**Tu app estará en:** http://TU_IP_DEL_VPS
