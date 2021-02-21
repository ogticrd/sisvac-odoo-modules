from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_vaccinator = fields.Boolean()
