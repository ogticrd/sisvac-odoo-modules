from odoo import fields, models, api, _


class Vaccination(models.TransientModel):
    _name = "sisvac.vaccination.wizard"
    _description = "Vaccination Wizard"

    appointment_id = fields.Many2one(
        "sisvac.vaccination.appointment",
        string="Appointment",
        required=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Vaccinator",
        required=True,
        default=lambda self: self.env.user.partner_id.id,
        domain="[('sisvac_is_vaccinator', '=', True)]",
    )
    application_date = fields.Datetime(default=fields.Datetime.now())
    product_id = fields.Many2one("product.product", related="lot_id.product_id")
    lot_id = fields.Many2one(
        "stock.production.lot",
        string="Lot",
        domain="[('company_id', '=', company_id)]",
        check_company=True,
    )
    symptoms = fields.Text()
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    def action_apply(self):
        self.ensure_one()
        application_obj = self.env["sisvac.vaccine.application"]
