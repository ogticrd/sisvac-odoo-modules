from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_vaccine = fields.Boolean()
    dosis_qty = fields.Integer()
    time_between_dose = fields.Integer()
    unit_time_between_dose = fields.Selection([
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("month", "Month"),
        ("years", "Years")
    ])
    frequency = fields.Integer()
    unit_frequency = fields.Selection([
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("month", "Month"),
        ("years", "Years")
    ])
