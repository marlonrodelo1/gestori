FROM odoo:18

# Copia la configuración de Odoo dentro de la imagen
# (list_db=False, dbfilter, log_level, etc.)
COPY config/odoo.conf /etc/odoo/odoo.conf

# Copia los addons personalizados de Gestori
COPY custom-addons/ /mnt/extra-addons/

# Copia el script de arranque que lee ADMIN_PASSWD desde Dokploy
COPY --chmod=755 scripts/start.sh /usr/local/bin/start.sh

# Arranca Odoo con la contraseña maestra desde variable de entorno
CMD ["/usr/local/bin/start.sh"]
