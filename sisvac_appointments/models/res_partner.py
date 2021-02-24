from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_vaccinator = fields.Boolean()
    vaccine_appointment_count = fields.Integer(
        compute='_compute_vaccine_appointment_count', string='Vaccine Appointment Count')
    vaccine_appointment_ids = fields.One2many('calendar.event', 'patient_id', 'Vaccine Appointment')

    def _compute_vaccine_appointment_count(self):
        for partner in self:
            partner.vaccine_appointment_count = len(partner.vaccine_appointment_ids)
