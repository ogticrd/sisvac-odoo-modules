import json
from odoo.http import request
from odoo.addons.component.core import Component


class LocationService(Component):
    _inherit = "base.rest.service"
    _name = "location.service"
    _usage = "location"
    _collection = "sisvac.services"
    _description = """
        Locations Related models API Services
    """

    def search(self):
        locations = self.env["stock.location"].search([("usage", "=", "internal")])
        return request.make_response(
            json.dumps([{"id": loc.id, "name": loc.name} for loc in locations]),
            headers=[("Content-Type", "application/json")],
        )


class LotsService(Component):
    _inherit = "base.rest.service"
    _name = "lots.service"
    _usage = "lots"
    _collection = "sisvac.services"
    _description = """
        Lots Related models API Services
    """

    def search(self):
        lots = self.env["stock.production.lot"].search([])  # add domain?
        return request.make_response(
            json.dumps(
                [
                    {
                        "id": lot.id,
                        "name": lot.name,
                        "ref": lot.ref,
                        "product_id": {
                            "id": lot.product_id.id,
                            "name": lot.product_id.name,
                        },
                        "product_qty": lot.product_qty,
                        "note": lot.note,
                    }
                    for lot in lots
                ]
            ),
            headers=[("Content-Type", "application/json")],
        )
