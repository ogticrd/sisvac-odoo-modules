from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class AppointmentsService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "appointments.service"
    _usage = "appointments"
    _collection = "sisvac.private.services"
    _description = """
        Appointments Related models API Services
    """

    def get(self, _id):
        appointment = self.env["sisvac.vaccination.appointment"].browse(_id)
        return self.response_wrapper(
            success=True,
            status=200,
            data=appointment._get_appointment_data(),
            headers=[("Content-Type", "application/json")],
        )

    def search(self, limit):
        appointment_obj = self.env["sisvac.vaccination.appointment"]
        if not limit:
            appointments = appointment_obj.search([])
        else:
            appointments = appointment_obj.search([], limit=limit)
        return self.response_wrapper(
            success=True,
            status=200,
            data=[apt._get_appointment_data() for apt in appointments],
            headers=[("Content-Type", "application/json")],
        )

    def _validator_search(self):
        return {
            "limit": {
                "type": "integer",
                "coerce": to_int,
            }
        }
