from odoo import models, fields


class Product(models.Model):
    _inherit = "product.template"

    sisvac_is_vaccine = fields.Boolean("Is vaccine?")
    sisvac_dose_qty = fields.Integer(default=1)

    sisvac_dose_interval = fields.Integer()
    sisvac_unit_time_between_dose = fields.Selection(
        [("days", "Days"), ("weeks", "Weeks"), ("months", "Month"), ("years", "Years")],
        default="days",
    )

    # TODO: what are these fields for?
    # sisvac_frequency = fields.Integer()
    # sisvac_unit_frequency = fields.Selection(
    #     [("days", "Days"), ("weeks", "Weeks"), ("month", "Month"), ("years", "Years")],
    #     default="days",
    # )
