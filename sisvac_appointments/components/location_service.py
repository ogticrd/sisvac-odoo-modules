from odoo.addons.component.core import Component

from .common import SisvacComponentsCommon

ResponseWrapper = SisvacComponentsCommon.response_wrapper


class LocationService(Component):
    _inherit = "base.rest.service"
    _name = "consent.service"
    _usage = "locations"
    _collection = "sisvac.services"
    _description = """
        Locations Related models API Services
    """

    def get(self, _id):
        locations = self.env["stock.location"].search([("sisvac_partner_id", "=", _id)])
        return ResponseWrapper(
            success=True,
            status=200,
            data=[loc._get_location_data() for loc in locations],
            headers=[("Content-Type", "application/json")],
        )
