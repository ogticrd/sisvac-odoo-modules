from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import to_int, to_bool


class LocationService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "location.service"
    _usage = "locations"
    _collection = "sisvac.private.services"
    _description = """
        Locations Related models API Services
    """

    def get(self, _id):
        locations = self.env["stock.location"].search([("sisvac_partner_id", "=", _id)])
        return self.response_wrapper(
            success=True,
            status=200,
            data=[loc._get_location_data() for loc in locations],
            headers=[("Content-Type", "application/json")],
        )

    def create(self, **params):
        Partner = self.env["res.partner"]
        partner_id = Partner.search([("ref", "=", params["center_id"])])
        if not partner_id:
            partner_id = Partner.create(
                {
                    "name": params["center_name"],
                    "ref": params["center_id"],
                    "sisvac_is_vaccination_center": True,
                }
            )

        self.env["stock.location"].create(
            {
                "name": params["center_name"],
                "usage": "internal",
                "sisvac_partner_id": partner_id.id,
            }
        )

        return self.response_wrapper(
            success=True,
            status=200,
            headers=[("Content-Type", "application/json")],
            message="Vaccination Center created",
        )

    def _validator_create(self):
        return {
            "center_id": {"type": "string", "required": True},
            "center_name": {"type": "string", "required": True},
            "municipality_data": {
                "type": "dict",
                "schema": {
                    "id": {"type": "string"},
                    "province": {"type": "string"},
                    "dps_das": {
                        "type": "dict",
                        "schema": {
                            "id": {"type": "integer", "coerce": to_int},
                            "name": {"type": "string"},
                        },
                    },
                },
            },
            "province_data": {
                "type": "dict",
                "schema": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "region": {"type": "string"},
                    "region_data": {
                        "type": "dict",
                        "schema": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                },
            },
            "available": {"type": "boolean", "required": True, "coerce": to_bool},
        }
