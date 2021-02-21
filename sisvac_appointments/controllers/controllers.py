from odoo.addons.base_rest.controllers import main


class RestController(main.RestController):
    _root_path = "/sisvac/"
    _collection_name = "sisvac.services"
