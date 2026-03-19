#!/bin/bash
# Script de arranque de Gestori
# Inyecta ADMIN_PASSWD desde Dokploy en el odoo.conf antes de arrancar.

set -e

if [ -z "$ADMIN_PASSWD" ]; then
    echo "ERROR: La variable ADMIN_PASSWD no está definida en Dokploy."
    exit 1
fi

# Añade admin_passwd al config en tiempo de ejecución (no se guarda en Git)
echo "admin_passwd = $ADMIN_PASSWD" >> /etc/odoo/odoo.conf

exec odoo
