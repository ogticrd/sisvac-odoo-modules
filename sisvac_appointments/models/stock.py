from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    sisvac_partner_id = fields.Many2one(
        "res.partner",
        string="Vaccination Center",
        domain="[('sisvac_is_vaccination_center', '=', True)]",
    )
