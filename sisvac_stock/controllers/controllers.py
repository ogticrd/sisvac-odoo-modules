from odoo.http import route
from odoo.addons.base_rest.controllers import main


class MyRestController(main.RestController):
    _root_path = "/sisvac/"
    _collection_name = "sisvac.services"
