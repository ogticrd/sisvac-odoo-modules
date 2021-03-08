from odoo import models, fields


class VaccinationConsent(models.Model):
    _name = "sisvac.vaccination.consent"
    _description = "Vaccination Consent"
    _rec_name = "partner_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(default=fields.Date.today(), copy=False)
    partner_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        domain="[('sisvac_is_patient', '=', True)]",
        copy=False
    )
    patient_signature = fields.Binary(copy=False)
    has_covid = fields.Boolean(copy=False)
    is_pregnant = fields.Boolean(copy=False)
    had_fever = fields.Boolean(copy=False)
    is_vaccinated = fields.Boolean(copy=False)
    had_reactions = fields.Boolean(copy=False)
    is_allergic = fields.Boolean(copy=False)
    is_medicated = fields.Boolean(copy=False)
    had_transplants = fields.Boolean(copy=False)

    def _get_consent_data(self):
        return {
            "id": self.id,
            "cedula": self.partner_id.vat,
            "name": self.partner_id.name,
            "age": self.partner_id.age,
            "has_covid": self.has_covid,
            "is_pregnant": self.is_pregnant,
            "had_fever": self.had_fever,
            "is_vaccinated": self.is_vaccinated,
            "had_reactions": self.had_reactions,
            "is_allergic": self.is_allergic,
            "is_medicated": self.is_medicated,
            "had_transplants": self.had_transplants,
        }
