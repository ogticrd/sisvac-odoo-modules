import json
from odoo.http import request
from odoo.addons.component.core import Component


class AppointmentsService(Component):
    _inherit = "base.rest.service"
    _name = "appointments.service"
    _usage = "appointments"
    _collection = "sisvac.services"
    _description = """
        Appointments Related models API Services
    """

    def get(self, _id):
        appointment = self.env["sisvac.vaccination.appointment"].browse(_id)
        return request.make_response(
            json.dumps(appointment._get_appointment_data()),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        appointment_obj = self.env["sisvac.vaccination.appointment"]
        if "limit" in params:
            appointments = appointment_obj.search([], limit=int(params["limit"]))
        else:
            appointments = appointment_obj.search([])
        return request.make_response(
            json.dumps([apt._get_appointment_data() for apt in appointments]),
            headers=[("Content-Type", "application/json")],
        )
