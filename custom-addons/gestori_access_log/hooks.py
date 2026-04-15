import random
from datetime import datetime, timedelta, time as dtime, date as ddate


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

    # Franjas horarias de entrada al sistema (lunes-viernes)
    FRANJAS = [
        (8, 9),    # Entrada mañana
        (13, 14),  # Después de comer
        (16, 18),  # Final de tarde
    ]

    # --- Accesos de lunes a viernes: 2-3 logins por día ---
    current_day = three_months_ago.date()
    end_day = now.date()

    while current_day <= end_day:
        # Solo días laborables (0=lunes, 4=viernes)
        if current_day.weekday() <= 4:
            accesos_hoy = random.randint(2, 3)
            franjas_hoy = random.sample(FRANJAS, min(accesos_hoy, len(FRANJAS)))

            for franja_inicio, franja_fin in franjas_hoy:
                hour = random.randint(franja_inicio, franja_fin - 1)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                log_date = datetime.combine(current_day, dtime(hour, minute, second))

                if log_date > now:
                    current_day += timedelta(days=1)
                    continue

                login, partner_id = random.choice(user_data)
                # 90% desde oficina, 10% remoto
                ip = random.choice(IPS_OFICINA + IPS_MOVIL if random.random() < 0.9 else IPS_REMOTO)
                result = 'success' if random.random() < 0.92 else 'failure'

                records.append({
                    'login': login,
                    'partner_id': partner_id if result == 'success' else False,
                    'ip': ip,
                    'result': result,
                    'date': log_date,
                })

        current_day += timedelta(days=1)

    # --- Intentos maliciosos aleatorios (bots, no respetan horario) ---
    for _ in range(40):
        days_back = random.randint(0, 90)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        log_date = three_months_ago + timedelta(days=days_back, hours=hour, minutes=minute)
        if log_date > now:
            log_date = now - timedelta(minutes=random.randint(10, 120))

        records.append({
            'login': random.choice(LOGINS_INVALIDOS),
            'partner_id': False,
            'ip': random.choice(IPS_SOSPECHOSAS),
            'result': 'failure',
            'date': log_date,
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
