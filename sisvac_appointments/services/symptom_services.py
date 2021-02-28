from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import to_int


class SymptomService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "symptoms.service"
    _usage = "symptoms"
    _collection = "sisvac.private.services"
    _description = """
        Symptom Related models API Services
    """

    def get(self, _id):
        symptom = self.env["sisvac.symptom"].browse(_id)
        return self.response_wrapper(
            success=True,
            status=200,
            data={"id": symptom.id, "name": symptom.name},
            headers=[("Content-Type", "application/json")],
        )

    def search(self, limit):
        symptom_obj = self.env["sisvac.symptom"]
        if not limit:
            symptoms = symptom_obj.search([])
        else:
            symptoms = symptom_obj.search([], limit=limit)

        return self.response_wrapper(
            success=True,
            status=200,
            data=[{"id": s.id, "name": s.name} for s in symptoms],
            headers=[("Content-Type", "application/json")],
        )

    def _validator_search(self):
        return {
            "limit": {
                "type": "integer",
                "coerce": to_int,
            }
        }
