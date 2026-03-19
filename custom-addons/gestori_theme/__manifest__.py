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
            ("prepend", "gestori_theme/static/src/scss/gestori_theme.scss"),
        ],
        "web.assets_frontend": [
            ("prepend", "gestori_theme/static/src/scss/gestori_theme.scss"),
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": True,
}
