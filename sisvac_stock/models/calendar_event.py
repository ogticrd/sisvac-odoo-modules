from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    product_id = fields.Many2one(
        "product.template", "Vaccine", readonly=True, domain=[("is_vaccine", "=", True)]
    )
    stock_move_id = fields.Many2one("stock.move", readonly=True)
    location_id = fields.Many2one(
        "stock.location", domain="[('usage', '=', 'internal')]"
    )
