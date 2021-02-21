import json
from odoo.http import request
from odoo.addons.component.core import Component


class LocationService(Component):
    _inherit = "base.rest.service"
    _name = "location.service"
    _usage = "location"
    _collection = "sisvac.services"
    _description = """
        Stock Related models API Services
    """

    def search(self):
        locations = self.env["stock.location"].search([("usage", "=", "internal")])
        return request.make_response(
            json.dumps([{"id": loc.id, "name": loc.name} for loc in locations]),
            headers=[("Content-Type", "application/json")],
        )
