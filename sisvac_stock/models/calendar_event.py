from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    product_id = fields.Many2one(
        "product.template", "Vaccine", readonly=True, domain=[("is_vaccine", "=", True)]
    )
    stock_move_id = fields.Many2one("stock.move", readonly=True)
    location_id = fields.Many2one(
        "stock.location",
        string="Vaccine Location",
        domain="[('usage', '=', 'internal')]",
    )

    product_image = fields.Binary("Vaccine photo", related="product_id.image_1024")
    product_dose_qty = fields.Integer("Dose Qty", related="product_id.dose_qty")
    product_time_between_dose = fields.Integer(
        "Time Between Dose", related="product_id.time_between_dose"
    )
    product_unit_time_between_dose = fields.Selection(
        related="product_id.unit_time_between_dose"
    )
    product_frequency = fields.Integer("Frequency", related="product_id.frequency")
    product_unit_frequency = fields.Selection(related="product_id.unit_frequency")
