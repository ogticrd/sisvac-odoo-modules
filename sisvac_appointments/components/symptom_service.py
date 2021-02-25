import json
from odoo.http import request
from odoo.addons.component.core import Component


class SymptomService(Component):
    _inherit = "base.rest.service"
    _name = "symptoms.service"
    _usage = "symptoms"
    _collection = "sisvac.services"
    _description = """
        Symptom Related models API Services
    """

    def get(self, _id):
        symptom = self.env["sisvac.symptom"].browse(_id)
        return request.make_response(
            json.dumps({"id": symptom.id, "name": symptom.name}),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        symptom_obj = self.env["sisvac.symptom"]
        if "limit" in params:
            symptoms = symptom_obj.search([], limit=int(params["limit"]))
        else:
            symptoms = symptom_obj.search([])
        return request.make_response(
            json.dumps([{"id": s.id, "name": s.name} for s in symptoms]),
            headers=[("Content-Type", "application/json")],
        )
