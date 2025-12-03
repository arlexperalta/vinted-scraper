#!/bin/bash

# Script de backup para datos del scraper
# Ejecutar en el VPS

echo "================================================"
echo "   VINTED SCRAPER - BACKUP"
echo "================================================"

# Crear directorio de backups si no existe
mkdir -p backups

# Nombre del archivo con timestamp
BACKUP_FILE="backups/vinted-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

# Crear backup
echo "Creando backup de datos..."
tar -czf "$BACKUP_FILE" data/

if [ $? -eq 0 ]; then
    echo "✓ Backup creado exitosamente: $BACKUP_FILE"

    # Mostrar tamaño
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "  Tamaño: $SIZE"

    # Limpiar backups antiguos (mantener últimos 7)
    echo ""
    echo "Limpiando backups antiguos (manteniendo últimos 7)..."
    ls -t backups/vinted-backup-*.tar.gz | tail -n +8 | xargs -r rm

    echo ""
    echo "Backups disponibles:"
    ls -lh backups/
else
    echo "✗ Error creando backup"
    exit 1
fi

echo ""
echo "================================================"
echo "Para restaurar un backup:"
echo "  tar -xzf $BACKUP_FILE"
echo "================================================"
