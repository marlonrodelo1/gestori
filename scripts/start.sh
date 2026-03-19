#!/bin/bash
# Script de arranque de Gestori
# Lee ADMIN_PASSWD desde las variables de entorno de Dokploy
# y lo pasa a Odoo como argumento seguro.

set -e

if [ -z "$ADMIN_PASSWD" ]; then
    echo "ERROR: La variable ADMIN_PASSWD no está definida en Dokploy."
    exit 1
fi

exec odoo --admin-passwd="$ADMIN_PASSWD"
