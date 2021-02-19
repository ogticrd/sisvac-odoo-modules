{
    'name': "SISVAC Appointments",
    'description': """
        Long description of module's purpose
    """,
    'author': "OPTIC, Kevin Jiménez",
    'website': "http://optic.gob.do",

    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'calendar', 'product'],

    'data': [
        'data/data.xml',
        'views/calendar_views.xml',
        'views/templates.xml',
    ]
}
