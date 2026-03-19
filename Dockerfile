FROM odoo:18

# Copia la configuración de Odoo dentro de la imagen
# (list_db=False, dbfilter, log_level, etc.)
COPY config/odoo.conf /etc/odoo/odoo.conf

# Copia el script de arranque que lee ADMIN_PASSWD desde Dokploy
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

# Arranca Odoo con la contraseña maestra desde variable de entorno
CMD ["/start.sh"]
