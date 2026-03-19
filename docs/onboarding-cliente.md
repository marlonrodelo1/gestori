# Onboarding de un cliente nuevo en Gestori

Pasos para dar de alta a un nuevo cliente en la plataforma.

---

## Requisitos previos

- Tener el nombre del cliente (sin espacios, solo letras minúsculas y guiones)
- Ejemplos válidos: `peluqueria`, `beta-corp`, `taller-juan`
- Ejemplos NO válidos: `Peluquería`, `taller juan`, `demo2025`

---

## Paso 1 — Crear la base de datos

1. Ve a `gestori.es/web/database/manager`
2. Pulsa **Create Database**
3. Rellena:
   - **Master Password:** (tu contraseña maestra de Dokploy)
   - **Database Name:** nombre del cliente (ej: `peluqueria`)
   - **Email:** email del administrador del cliente
   - **Password:** contraseña inicial del administrador del cliente
   - **Language:** Spanish (ES)
   - **Country:** Spain
   - **Demo Data:** NO marcar
4. Pulsa **Create Database** y espera 1-2 minutos

---

## Paso 2 — Añadir el subdominio en Dokploy

1. Abre Dokploy → Proyecto **Gestori** → servicio **Fronted**
2. Pestaña **Domains** → pulsa **Add Domain**
3. Rellena:
   - **Domain:** `nombrecliente.gestori.es` (ej: `peluqueria.gestori.es`)
   - **Port:** 8069
   - **HTTPS:** activado
   - **Cert:** letsencrypt
4. Guarda y espera 1-2 minutos a que el certificado SSL se genere

---

## Paso 3 — Verificar que funciona

1. Abre `nombrecliente.gestori.es` en el navegador
2. Debe aparecer la pantalla de login de Odoo
3. Inicia sesión con el email y contraseña que pusiste en el Paso 1
4. Verifica que el candado HTTPS aparece en el navegador

---

## Paso 4 — Entregar acceso al cliente

Envía al cliente:

```
URL de acceso: https://nombrecliente.gestori.es
Usuario: email que pusiste en el Paso 1
Contraseña: contraseña que pusiste en el Paso 1
```

---

## Gestión de la base de datos del cliente

Para hacer backup, duplicar o eliminar la base de datos de un cliente:

- Ve a `nombrecliente.gestori.es/web/database/manager`
- Introduce la Master Password
- Desde ahí puedes hacer Backup, Duplicate o Delete

---

## Nombres reservados (NO usar como nombre de cliente)

- `gestori` — base de datos principal
- `demo` — entorno de demostración
- `www` — reservado
- `admin` — reservado
- `staging` — reservado para pruebas

---

## Resolución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| La URL del cliente da 404 | El dominio no está añadido en Dokploy | Repetir Paso 2 |
| "Database does not exist" | El nombre de la base de datos no coincide con el subdominio | Verificar que el nombre es exactamente igual |
| SSL no funciona (candado rojo) | El certificado aún no se ha generado | Esperar 2-5 minutos y recargar |
| No puedo entrar al manager | Estás usando el subdominio equivocado | Usar `nombrecliente.gestori.es/web/database/manager` |
