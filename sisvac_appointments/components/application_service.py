import json
from odoo.http import request
from odoo.addons.component.core import Component


class ApplicationService(Component):
    _inherit = "base.rest.service"
    _name = "application.service"
    _usage = "application"
    _collection = "sisvac.services"
    _description = """
        Vaccines Application Related models API Services
    """

    def get(self, _id):
        application = self.env["sisvac.vaccine.application"].browse(_id)
        return request.make_response(
            json.dumps(application._get_application_data()),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        application_obj = self.env["sisvac.vaccine.application"]
        if "limit" in params:
            applications = application_obj.search([], limit=int(params["limit"]))
        else:
            applications = application_obj.search([])
        return request.make_response(
            json.dumps([app._get_application_data() for app in applications]),
            headers=[("Content-Type", "application/json")],
        )
