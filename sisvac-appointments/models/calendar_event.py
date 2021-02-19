from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    appointment_number = fields.Char(readonly=True, default="New")
    patient_id = fields.Many2one("res.partner")
    next_appointment_date = fields.Datetime(readonly=True)
    vaccination_appointment = fields.Boolean(readonly=True)
    product_id = fields.Many2one("product.template", "Vaccine", readonly=True, domain=[("is_vaccine", "=", True)])
    state = fields.Selection([
        ("pending", "Pending"),
        ("done", "Done"),
        ("canceled", "Canceled")
    ], default="pending", readonly=True)
    dosis_number = fields.Integer(readonly=True)
    stock_move_id = fields.Many2one("stock.move", readonly=True)
    another_appointment_needed = fields.Boolean(readonly=True)
    lots = fields.Char(readonly=True)
    vaccinator_id = fields.Many2one("res.partner", readonly=True, domain=[("is_vaccinator", "=", True)])
    patient_firm = fields.Binary(readonly=True)
    got_symptoms = fields.Boolean("Got Symptoms?", readonly=True)
    symptoms = fields.Text(readonly=True)
    location_id = fields.Many2one("stock.location", domain="[('usage', '=', 'internal')]")

    @api.model
    def create(self, vals):
        if vals.get("appointment_number", "New") == "New":
            vals["appointment_number"] = self.env['ir.sequence'].next_by_code('sisvac.appointment') or "/"
            vals["name"] = vals["appointment_number"]
        return super(CalendarEvent, self).create(vals)

    @api.constrains('patient_id', 'status', 'vaccination_appointment')
    def _check_sigle_active_appointment(self):
        for record in self:
            appointment_filter = [
                ("vaccination_appointment", "=", True),
                ("status", "=", "pending"),
                ("patient_id", "=", record.patient_id.id)
            ]

            current_appointments = self.search_count(appointment_filter)

            if current_appointments > 1:
                raise ValidationError(_("This patient have another active vaccination appointment. \
                    \nEach patient only can have one active vaccination appointment."))

    def action_put_vaccine(self):

        return {
            'name': _('Put Vaccine'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sisvac.vaccination.wizard',
            'target': 'new'
        }
