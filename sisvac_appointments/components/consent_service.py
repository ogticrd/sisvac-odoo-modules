import json
from odoo.http import request
from odoo.addons.component.core import Component


class ConsentService(Component):
    _inherit = "base.rest.service"
    _name = "consent.service"
    _usage = "consents"
    _collection = "sisvac.services"
    _description = """
        Consent Related models API Services
    """

    def get(self, _id):
        consent = self.env["sisvac.vaccination.consent"].browse(_id)
        return request.make_response(
            json.dumps(consent._get_consent_date()),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        consent_obj = self.env["sisvac.vaccination.consent"]
        if "limit" in params:
            consents = consent_obj.search([], limit=int(params["limit"]))
        else:
            consents = consent_obj.search([])
        return request.make_response(
            json.dumps([c._get_consent_date() for c in consents]),
            headers=[("Content-Type", "application/json")],
        )
