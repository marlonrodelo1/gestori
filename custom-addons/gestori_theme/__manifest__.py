{
    "name": "Gestori Theme",
    "summary": "Colores, logo y branding de Gestori",
    "version": "18.0.1.0.0",
    "category": "Theme",
    "author": "Gestori",
    "license": "LGPL-3",
    "depends": ["web"],
    "data": [
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_web": [
            "gestori_theme/static/src/css/gestori_theme.css",
        ],
        "web.assets_frontend": [
            "gestori_theme/static/src/css/gestori_theme.css",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": True,
}
