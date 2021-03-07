from odoo.addons.base_rest.controllers import main


class RestPrivateController(main.RestController):
    _root_path = "/sisvac/"
    _collection_name = "sisvac.private.services"
    _default_auth = "user"


class RestPublicController(main.RestController):
    _root_path = "/sisvac/"
    _collection_name = "sisvac.public.services"
    _default_auth = "public"
