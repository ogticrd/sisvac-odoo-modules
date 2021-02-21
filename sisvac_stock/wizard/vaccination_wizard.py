from odoo import fields, models


class Vaccination(models.TransientModel):
    _inherit = "sisvac.vaccination.wizard"

    product_id = fields.Many2one(
        "product.template", "Vaccine", domain=[("is_vaccine", "=", True)]
    )

    def _get_vaccination_data(self):
        res = super(Vaccination, self)._get_vaccination_data()
        res["product_id"] = self.product_id.id
        return res
