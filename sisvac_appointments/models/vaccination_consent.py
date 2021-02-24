from odoo import models, fields


class VaccinationConsent(models.Model):
    _name = "sisvac.vaccination.consent"
    _description = "Vaccination Consent"
    _rec_name = "partner_id"

    date = fields.Date(default=fields.Date.today())
    partner_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        domain="[('sisvac_is_patient', '=', True)]",
    )
    patient_signature = fields.Binary()
    has_covid = fields.Boolean()
    is_pregnant = fields.Boolean()
    had_fever = fields.Boolean()
    is_vaccinated = fields.Boolean()
    had_reactions = fields.Boolean()
    is_allergic = fields.Boolean()
    is_medicated = fields.Boolean()
    had_transplants = fields.Boolean()

    def _get_consent_date(self):
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
