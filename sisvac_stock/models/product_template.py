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

    product_image = fields.Binary("Vaccine photo", related="product_id.image_1024")
    product_dose_qty = fields.Integer("Dose Qty", related="product_id.dose_qty")
    product_time_between_dose = fields.Integer(
        "Time Between Dose", related="product_id.time_between_dose"
    )
    product_unit_time_between_dose = fields.Selection(
        "Unit time between dose", related="product_id.unit_time_between_dose"
    )
    product_frequency = fields.Integer("Frequency", related="product_id.frequency")
    product_unit_frequency = fields.Selection(
        "Unit Frequency", related="product_id.unit_frequency"
    )
