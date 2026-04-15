import random
from datetime import datetime, timedelta


# IPs realistas: oficina, móviles, remotos, intentos maliciosos
IPS_OFICINA = [
    '85.84.12.33',   # Oficina principal
    '85.84.12.34',
    '212.166.45.78', # Sede secundaria
    '192.168.1.105', # Red interna
    '192.168.1.110',
    '192.168.1.115',
]
IPS_MOVIL = [
    '80.58.134.22',  # Movistar España
    '80.58.134.89',
    '88.26.121.44',  # Vodafone España
    '88.26.121.51',
    '95.120.33.17',  # Orange España
    '217.216.45.9',
]
IPS_REMOTO = [
    '37.235.1.174',  # VPN común
    '46.19.37.108',
    '178.33.21.9',
    '91.108.56.100',
]
IPS_SOSPECHOSAS = [
    '185.220.101.5',   # Tor exit node
    '185.220.101.34',  # Tor exit node
    '45.33.32.156',    # Scanner conocido
    '198.51.100.42',   # Scanner conocido
    '203.0.113.195',   # Rusia
    '103.21.244.0',    # China
    '5.188.206.26',    # Botnet conocida
]

LOGINS_VALIDOS = [
    'admin',
    'marlon@empresa.es',
    'info@empresa.es',
    'ventas@empresa.es',
    'contabilidad@empresa.es',
    'soporte@empresa.es',
    'gerencia@empresa.es',
]

LOGINS_INVALIDOS = [
    'administrator',
    'root',
    'test',
    'user',
    'admin@admin.com',
    'hacker@spam.ru',
    'info@empresa.es',   # login válido pero desde IP sospechosa
]


def _generate_demo_logs(env):
    """Genera ~450 registros de acceso de los últimos 3 meses."""
    now = datetime.now()
    three_months_ago = now - timedelta(days=90)

    # Usar solo usuarios cuyo email pertenece al dominio de la compañía principal
    main_company = env.ref('base.main_company', raise_if_not_found=False)
    company_domain = ''
    if main_company:
        if main_company.email and '@' in main_company.email:
            company_domain = main_company.email.split('@')[1]
        elif main_company.website:
            company_domain = (
                main_company.website
                .replace('https://', '').replace('http://', '')
                .replace('www.', '').strip('/')
            )

    if company_domain:
        users = env['res.users'].search([
            ('active', '=', True),
            ('share', '=', False),
            ('login', 'like', '@' + company_domain),
        ], limit=10)
    else:
        users = env['res.users'].search([
            ('active', '=', True),
            ('share', '=', False),
            ('company_id', '=', main_company.id if main_company else False),
        ], limit=10)

    user_data = [(u.login, u.partner_id.id) for u in users if u.partner_id and u.login]
    if not user_data:
        # Fallback: cualquier usuario interno
        fallback = env['res.users'].search([('active', '=', True), ('share', '=', False)], limit=1)
        user_data = [(fallback[0].login, fallback[0].partner_id.id)] if fallback else [('admin', False)]

    records = []

    # --- Accesos normales de oficina (60%) ---
    for _ in range(270):
        days_back = random.randint(0, 90)
        hour = random.randint(8, 19)
        minute = random.randint(0, 59)
        log_date = three_months_ago + timedelta(days=days_back, hours=hour - 8, minutes=minute)
        if log_date > now:
            log_date = now - timedelta(minutes=random.randint(5, 120))

        login, partner_id = random.choice(user_data)
        ip = random.choice(IPS_OFICINA + IPS_MOVIL)
        result = 'success' if random.random() < 0.92 else 'failure'

        records.append({
            'login': login,
            'partner_id': partner_id if result == 'success' else False,
            'ip': ip,
            'result': result,
            'create_date': log_date,
        })

    # --- Accesos remotos (20%) ---
    for _ in range(90):
        days_back = random.randint(0, 90)
        hour = random.randint(7, 23)
        minute = random.randint(0, 59)
        log_date = three_months_ago + timedelta(days=days_back, hours=hour - 7, minutes=minute)
        if log_date > now:
            log_date = now - timedelta(minutes=random.randint(5, 60))

        login, partner_id = random.choice(user_data)
        ip = random.choice(IPS_REMOTO)
        result = 'success' if random.random() < 0.80 else 'failure'

        records.append({
            'login': login,
            'partner_id': partner_id if result == 'success' else False,
            'ip': ip,
            'result': result,
            'create_date': log_date,
        })

    # --- Intentos maliciosos (20%) - siempre fallan ---
    for _ in range(90):
        days_back = random.randint(0, 90)
        # Los bots atacan a cualquier hora
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        log_date = three_months_ago + timedelta(days=days_back, hours=hour, minutes=minute, seconds=second)
        if log_date > now:
            log_date = now - timedelta(seconds=random.randint(60, 3600))

        login = random.choice(LOGINS_INVALIDOS)
        ip = random.choice(IPS_SOSPECHOSAS)

        records.append({
            'login': login,
            'partner_id': False,
            'ip': ip,
            'result': 'failure',
            'create_date': log_date,
        })

    # Ordenar cronológicamente
    records.sort(key=lambda r: r['create_date'])

    for rec in records:
        env['gestori.access.log'].sudo().create(rec)


def post_init_hook(env):
    """Se ejecuta al instalar el módulo. Genera datos demo si no hay registros."""
    existing = env['gestori.access.log'].search_count([])
    if existing == 0:
        _generate_demo_logs(env)
