{
    "name": "SISVAC Appointments",
    "description": """
        SISVAC Appointments
    """,
    "author": "OPTIC, Kevin Jiménez",
    "website": "http://optic.gob.do",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": [
        "base",
        "stock",
        "calendar",
        "base_rest",
        "base_rest_datamodel",
        "partner_contact_gender",
        "partner_contact_age_range",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/symptom_data.xml",
        "views/appointment_views.xml",
        "views/application_views.xml",
        "views/partner_views.xml",
        "views/symptom_views.xml",
        "views/consent_views.xml",
        "views/stock_views.xml",
        "views/product_views.xml",
    ],
    "demo": [
        "demo/product_demo_data.xml",
        "demo/partner_demo_data.xml",
    ],
    "installable": True,
    "application": True,
}
