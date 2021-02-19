from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    appointment_number = fields.Char(readonly=True, default="New")
    patient_id = fields.Many2one("res.partner")
    next_appointment_date = fields.Datetime(readonly=True)
    vaccination_appointment = fields.Boolean(readonly=True)
    product_id = fields.Many2one("product.template", "Vaccine", domain=[("is_vaccine", "=", True)])
    status = fields.Selection([
        ("pending", "Pending"),
        ("done", "Done"),
        ("canceled", "Canceled")
    ], default="pending")
    dosis_number = fields.Integer(readonly=True)
    stock_move_id = fields.Many2one("stock.move", readonly=True)
    another_appointment_needed = fields.Boolean(readonly=True)

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
