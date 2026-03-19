{
    "name": "Gestori - Registro de Accesos",
    "summary": "Log de accesos con IP y exportación a PDF",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "author": "Gestori",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "report/access_log_report.xml",
        "views/access_log_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
