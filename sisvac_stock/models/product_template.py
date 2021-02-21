from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_vaccine = fields.Boolean()
    dose_qty = fields.Integer(default=1)
    time_between_dose = fields.Integer()
    unit_time_between_dose = fields.Selection(
        [("days", "Days"), ("weeks", "Weeks"), ("month", "Month"), ("years", "Years")],
        default="days",
    )
    frequency = fields.Integer()
    unit_frequency = fields.Selection(
        [("days", "Days"), ("weeks", "Weeks"), ("month", "Month"), ("years", "Years")],
        default="days",
    )
