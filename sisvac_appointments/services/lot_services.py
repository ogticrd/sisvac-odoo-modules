from odoo import fields
from odoo.addons.component.core import Component


class LotService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "consent.service"
    _usage = "lots"
    _collection = "sisvac.services"
    _description = """
        Lots Related models API Services
    """

    def get(self, _id):
        lots = self.env["stock.production.lot"].search([("product_id", "=", _id)])
        return self.response_wrapper(
            success=True,
            status=200,
            data=[
                {
                    "id": lot.id,
                    "vaccine": lot.product_id.id,
                    "days_between_dose": lot.product_id.sisvac_unit_time_between_dose,
                    "next_date": self.env[
                        "sisvac.vaccination.appointment"
                    ]._get_next_appointment_date(
                        fields.Datetime.now(),
                        lot.product_id.sisvac_dose_interval,
                        lot.product_id.sisvac_unit_time_between_dose,
                    ),
                }
                for lot in lots
            ],
            headers=[("Content-Type", "application/json")],
        )
