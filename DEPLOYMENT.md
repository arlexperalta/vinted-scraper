# Guía de Deployment - Vinted Scraper VPS

Esta guía te ayudará a desplegar tu aplicación en un VPS usando Docker y Nginx.

## Requisitos Previos

- VPS con Ubuntu 20.04+ o Debian 11+ (mínimo 2GB RAM recomendado)
- Acceso SSH al VPS
- Docker y Docker Compose instalados en el VPS
- (Opcional) Dominio apuntando a la IP del VPS

---

## Paso 1: Preparar el VPS

### 1.1 Conectarse al VPS

```bash
ssh usuario@tu-ip-del-vps
```

### 1.2 Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Instalar Docker

```bash
# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Añadir repositorio de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Añadir tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Reiniciar la sesión o ejecutar:
newgrp docker
```

### 1.4 Instalar Docker Compose

```bash
# Descargar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

---

## Paso 2: Subir el Proyecto al VPS

### Opción A: Usando Git (Recomendado)

1. **Crear repositorio en GitHub** (si no lo has hecho):
   ```bash
   # En tu PC local
   cd C:\Users\arlex\Documents\vinted-scraper
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/vinted-scraper.git
   git push -u origin main
   ```

2. **Clonar en el VPS**:
   ```bash
   # En el VPS
   cd ~
   git clone https://github.com/TU-USUARIO/vinted-scraper.git
   cd vinted-scraper
   ```

### Opción B: Usando SCP

```bash
# En tu PC local (PowerShell o CMD)
scp -r C:\Users\arlex\Documents\vinted-scraper usuario@tu-ip-del-vps:~/
```

---

## Paso 3: Configurar la Aplicación

### 3.1 Editar configuración de Nginx (opcional)

```bash
# En el VPS
nano nginx/nginx.conf
```

Cambia `server_name _;` por tu dominio o déjalo como está si usas solo IP:
```nginx
server_name tu-dominio.com;  # o déjalo como _ para usar IP
```

### 3.2 Abrir puertos en el firewall

```bash
# Si usas UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Si usas iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

---

## Paso 4: Deployment

### 4.1 Ejecutar el script de deployment

```bash
# En el VPS, dentro del directorio del proyecto
chmod +x deploy.sh
./deploy.sh
```

El script automáticamente:
- Construirá las imágenes Docker
- Creará los contenedores
- Iniciará nginx y la aplicación Flask

### 4.2 Verificar que todo funciona

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver estado de los contenedores
docker-compose ps

# Debería mostrar algo como:
# NAME              COMMAND                  SERVICE   STATUS
# vinted-scraper    "python app.py"          web       running
# vinted-nginx      "/docker-entrypoint.…"   nginx     running
```

---

## Paso 5: Acceder a la Aplicación

Abre tu navegador y visita:
- **Con IP**: `http://TU_IP_DEL_VPS`
- **Con dominio**: `http://tu-dominio.com`

Deberías ver la interfaz web del scraper.

---

## Configuración SSL/HTTPS (Opcional pero Recomendado)

### Usando Let's Encrypt (Gratis)

1. **Instalar Certbot**:
   ```bash
   sudo apt install -y certbot
   ```

2. **Detener nginx temporalmente**:
   ```bash
   docker-compose stop nginx
   ```

3. **Obtener certificado**:
   ```bash
   sudo certbot certonly --standalone -d tu-dominio.com
   ```

4. **Copiar certificados**:
   ```bash
   sudo mkdir -p nginx/ssl
   sudo cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem nginx/ssl/certificate.crt
   sudo cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem nginx/ssl/private.key
   sudo chown -R $USER:$USER nginx/ssl
   ```

5. **Descomentar sección HTTPS en nginx.conf**:
   ```bash
   nano nginx/nginx.conf
   ```

   Descomenta las líneas del servidor HTTPS (las que están con `#`).

6. **Reiniciar servicios**:
   ```bash
   docker-compose up -d
   ```

---

## Comandos Útiles

### Gestión de contenedores

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Iniciar servicios
docker-compose up -d

# Rebuild después de cambios
docker-compose up -d --build
```

### Actualizar la aplicación

```bash
# Si usas Git
git pull origin main
./deploy.sh

# O manualmente
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Ver uso de recursos

```bash
# CPU y memoria de los contenedores
docker stats

# Espacio en disco
docker system df
```

### Backup de datos

```bash
# Crear backup del directorio de datos
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Restaurar backup
tar -xzf backup-YYYYMMDD.tar.gz
```

---

## Troubleshooting

### La aplicación no responde

```bash
# Verificar logs
docker-compose logs web

# Verificar que el contenedor está corriendo
docker-compose ps

# Reiniciar el servicio
docker-compose restart web
```

### Error de memoria

Si el VPS tiene poca RAM, Playwright puede fallar:

```bash
# Añadir swap (memoria virtual)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Hacer permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Puerto 80 ocupado

```bash
# Ver qué está usando el puerto 80
sudo lsof -i :80

# Detener apache2 si está instalado
sudo systemctl stop apache2
sudo systemctl disable apache2
```

### Actualizar solo nginx

```bash
docker-compose restart nginx
```

---

## Configuración Automática de Reinicio

Para que la aplicación se reinicie automáticamente después de un reinicio del servidor:

```bash
# Habilitar Docker al inicio
sudo systemctl enable docker

# Los contenedores ya tienen restart: unless-stopped en docker-compose.yml
```

---

## Monitoreo (Opcional)

### Instalar Portainer (UI para Docker)

```bash
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce

# Accede a: http://TU_IP_DEL_VPS:9000
```

---

## Resumen

1. ✅ Instalar Docker y Docker Compose en el VPS
2. ✅ Subir el proyecto (Git o SCP)
3. ✅ Configurar nginx.conf con tu dominio/IP
4. ✅ Ejecutar `./deploy.sh`
5. ✅ Acceder a `http://TU_IP_DEL_VPS`
6. ✅ (Opcional) Configurar SSL con Let's Encrypt

---

## Contacto y Soporte

Si tienes problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica que los puertos 80 y 443 están abiertos
3. Asegúrate de tener suficiente RAM (mínimo 2GB)

Listo para compartir con tu amigo! 🚀
