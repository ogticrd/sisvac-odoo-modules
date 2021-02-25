from odoo.addons.component.core import Component

from .common import SisvacComponentsCommon

ResponseWrapper = SisvacComponentsCommon.response_wrapper


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
        return ResponseWrapper(
            success=True,
            status=200,
            data={"id": symptom.id, "name": symptom.name},
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        symptom_obj = self.env["sisvac.symptom"]
        if "limit" in params:
            symptoms = symptom_obj.search([], limit=int(params["limit"]))
        else:
            symptoms = symptom_obj.search([])

        return ResponseWrapper(
            success=True,
            status=200,
            data=[{"id": s.id, "name": s.name} for s in symptoms],
            headers=[("Content-Type", "application/json")],
        )
