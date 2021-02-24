{
    "name": "SISVAC Appointments",
    "description": """
        SISVAC Appointments
    """,
    "author": "OPTIC, Kevin Jiménez",
    "website": "http://optic.gob.do",
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["calendar", "base_rest"],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/calendar_views.xml",
        "views/res_partner.xml",
        "views/symptoms.xml",
        "wizard/vaccination_wizard.xml",
    ],
}
