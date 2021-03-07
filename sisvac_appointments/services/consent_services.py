from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import to_bool, to_int


class ConsentService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "consent.service"
    _usage = "consents"
    _collection = "sisvac.private.services"
    _description = """
        Consent Related models API Services
    """

    def get(self, _id):
        consent = self.env["sisvac.vaccination.consent"].browse(_id)
        return self.response_wrapper(
            success=True,
            status=200,
            data=consent._get_consent_data(),
            headers=[("Content-Type", "application/json")],
        )

    def search(self, limit):
        consent_obj = self.env["sisvac.vaccination.consent"]
        if not limit:
            consents = consent_obj.search([])
        else:
            consents = consent_obj.search([], limit=limit)
        return self.response_wrapper(
            success=True,
            status=200,
            data=[c._get_consent_data() for c in consents],
            headers=[("Content-Type", "application/json")],
        )

    def _validator_search(self):
        return {
            "limit": {
                "type": "integer",
                "coerce": to_int,
            }
        }

    def create(self, **params):

        Partner = self.env["res.partner"]
        vat = params["cedula"]
        partner_id = Partner.search([("vat", "=", vat)], limit=1)
        if not partner_id:
            partner_id = Partner.create({"name": params.get("name"), "vat": vat})

        consent_id = self.env["sisvac.vaccination.consent"].create(
            {
                "partner_id": partner_id.id,
                "patient_signature": params.get("patient_signature"),
                "has_covid": params.get("has_covid"),
                "is_pregnant": params.get("is_pregnant"),
                "had_fever": params.get("had_fever"),
                "is_vaccinated": params.get("is_vaccinated"),
                "had_reactions": params.get("had_reactions"),
                "is_allergic": params.get("is_allergic"),
                "is_medicated": params.get("is_medicated"),
                "had_transplants": params.get("had_transplants"),
            }
        )

        return self.response_wrapper(
            success=True,
            status=200,
            data=consent_id._get_consent_data(),
            headers=[("Content-Type", "application/json")],
        )

    def _validator_create(self):
        return {
            "cedula": {"type": "string", "required": True},
            "has_covid": {"type": "boolean", "required": False, "coerce": to_bool},
            "is_pregnant": {"type": "boolean", "required": False, "coerce": to_bool},
            "had_fever": {"type": "boolean", "required": False, "coerce": to_bool},
            "is_vaccinated": {"type": "boolean", "required": False, "coerce": to_bool},
            "had_reactions": {"type": "boolean", "required": False, "coerce": to_bool},
            "is_allergic": {"type": "boolean", "required": False, "coerce": to_bool},
            "is_medicated": {"type": "boolean", "required": False, "coerce": to_bool},
            "had_transplants": {
                "type": "boolean",
                "required": False,
                "coerce": to_bool,
            },
        }
