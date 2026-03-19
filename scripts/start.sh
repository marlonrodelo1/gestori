#!/bin/bash
# Script de arranque de Gestori
# Inyecta ADMIN_PASSWD desde Dokploy en el odoo.conf antes de arrancar.

set -e

if [ -z "$ADMIN_PASSWD" ]; then
    echo "ERROR: La variable ADMIN_PASSWD no está definida en Dokploy."
    exit 1
fi

# Copia el config a /tmp (escribible por el usuario odoo) y añade admin_passwd
cp /etc/odoo/odoo.conf /tmp/odoo-runtime.conf
echo "admin_passwd = $ADMIN_PASSWD" >> /tmp/odoo-runtime.conf

exec odoo --config=/tmp/odoo-runtime.conf
