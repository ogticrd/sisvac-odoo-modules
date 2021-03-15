from odoo import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    sisvac_partner_id = fields.Many2one(
        "res.partner",
        string="Vaccination Center",
        domain="[('sisvac_is_vaccination_center', '=', True)]",
    )

    _sql_constraints = [
        (
            "unique_sisvac_partner_id",
            "UNIQUE (sisvac_partner_id)",
            "Only one location per Vaccination Center is allowed",
        )
    ]

    def _get_location_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.sisvac_partner_id.partner_latitude,
            "longitude": self.sisvac_partner_id.partner_longitude,
        }
