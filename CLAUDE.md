# CLAUDE.md — Proyecto Gestori

## Descripción
Plataforma multi-tenant de Odoo 18 Community. Cada cliente tiene su propia base de datos.
Desplegado en Dokploy con Docker. Repositorio: `marlonrodelo1/gestori`, rama `18.0`.

## Infraestructura
- **Odoo**: contenedor `gestori-fronted-bxg95k` (servicio "Fronted" en Dokploy)
- **PostgreSQL**: contenedor `gestori-gestoridb-k36tcn`, host interno `gestori-gestoridb-k36tcn`, puerto `5432`
- **DB user**: `odoo` / contraseña en variable de entorno `PASSWORD`
- **Addons personalizados**: `/mnt/extra-addons/` dentro del contenedor de Odoo
- **Deploy automático**: Dokploy despliega en cada push a rama `18.0` (Trigger: On Push)

## Bases de datos de clientes
| BD | URL |
|---|---|
| Rogotech | rogotech.gestori.es |
| belgique | belgique.gestori.es |
| demo | demo.gestori.es |
| gestori | gestori.gestori.es |
| ignacio | ignacio.gestori.es |
| luampa | luampa.gestori.es |
| revolution | revolution.gestori.es |

## Comandos útiles en el contenedor de Odoo

### Actualizar módulo en todas las BDs
```bash
for db in Rogotech belgique demo gestori ignacio luampa revolution; do
  odoo -d $db -u <modulo> --stop-after-init --no-http \
    --db_host=gestori-gestoridb-k36tcn --db_port=5432 \
    --db_user=odoo --db_password='@Pocho123' 2>&1 | tail -2
done
```

### Instalar módulo en todas las BDs
```bash
for db in Rogotech belgique demo gestori ignacio luampa revolution; do
  odoo -d $db -i <modulo> --stop-after-init --no-http \
    --db_host=gestori-gestoridb-k36tcn --db_port=5432 \
    --db_user=odoo --db_password='@Pocho123' 2>&1 | tail -2
done
```

### Ejecutar script Python en una BD
```bash
odoo shell -d <bd> --no-http \
  --db_host=gestori-gestoridb-k36tcn --db_port=5432 \
  --db_user=odoo --db_password='@Pocho123' <<'EOF'
# código python aquí
env.cr.commit()
EOF
```

### Regenerar datos demo en todas las BDs
```bash
for db in Rogotech belgique demo gestori ignacio luampa revolution; do
  odoo shell -d $db --no-http \
    --db_host=gestori-gestoridb-k36tcn --db_port=5432 \
    --db_user=odoo --db_password='@Pocho123' <<'EOF'
env['gestori.access.log'].sudo().search([]).unlink()
env.cr.commit()
from odoo.addons.gestori_access_log.hooks import _generate_demo_logs
_generate_demo_logs(env)
env.cr.commit()
print("OK")
EOF
done
```

## Módulos personalizados

### gestori_access_log
- **Modelo**: `gestori.access.log` — registra logins con IP, usuario, resultado y fecha
- **Campo fecha**: `date` (campo propio, no `create_date`)
- **Hook**: `post_init_hook` exportado desde `__init__.py`
- **Datos demo**: genera accesos de lunes a viernes, 2-3 por día, últimos 3 meses
  - Filtra usuarios por dominio del email de la compañía principal
  - IPs realistas: oficina, móvil, remoto, sospechosas (bots/Tor)
- **Menú**: Gestori → Registros de Acceso
- **Generar datos**: URL directa `/odoo/action-gestori_access_log.action_generate_demo_wizard`
- **Exportar**: PDF (botón Imprimir) + Excel (Acción → Exportar)
- **Filtros**: Hoy / Esta semana / Este mes / Últimos 3 meses
- **Vistas**: Lista, Gráfico, Pivot

## Notas importantes
- Los archivos en `/mnt/extra-addons/` son de solo lectura para el usuario `odoo` — no se pueden editar desde el contenedor
- Siempre usar `--no-http` con `--stop-after-init` para evitar conflicto de puertos (Odoo ya corre en el contenedor)
- El warning `Warn: Can't find .pfb for face 'Courier'` es inofensivo
- `belgique` y otras BDs pueden tener usuarios de múltiples compañías — los datos demo filtran por dominio del email de la compañía principal
- Módulo `access_log_viewer` estaba instalado en `ignacio` y `luampa` como huérfano — desactivado con SQL
