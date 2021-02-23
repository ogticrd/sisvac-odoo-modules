from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class VaccineApplication(models.Model):
    _name = "sisvac.vaccine.application"
    _description = "Vaccine Application"
    _order = "application_date"

    appointment_id = fields.Many2one(
        "sisvac.vaccination.appointment",
        string="Appointment",
        required=True,
    )
    application_date = fields.Datetime()
    state = fields.Selection(
        [("draft", "Draft"), ("scheduled", "Scheduled"), ("applied", "Applied")],
        draft="draft",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        related="appointment_id.product_id",
        store=True,
        readonly=True,
    )
    lot_id = fields.Many2one(
        "stock.production.lot",
        string="Lot",
        domain="[('product_id','=', product_id), ('company_id', '=', company_id)]",
        check_company=True,
    )
    symptoms = fields.Text(readonly=True)  # consider use M2M
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )


class VaccinationAppointment(models.Model):
    _name = "sisvac.vaccination.appointment"
    _description = "Vaccination Appointment"
    _inherit = "mail.thread"
    _order = "next_appointment_date, name"

    name = fields.Char(required=True, string="Appointment Number")
    patient_id = fields.Many2one("res.partner", string="Patient")
    patient_signature = fields.Binary()
    observations = fields.Text()
    # patient_image = fields.Binary("Patient photo", related="patient_id.image_1024")
    # patient_vat = fields.Char(related="patient_id.vat")
    vaccinator_id = fields.Many2one(
        "res.partner", string="Vaccinator", domain=[("is_vaccinator", "=", True)]
    )
    last_appointment_date = fields.Datetime()
    next_appointment_date = fields.Datetime()
    current_application_id = fields.Many2one(
        "sisvac.vaccine.application", string="Current Application", required=True
    )
    application_ids = fields.One2many(
        "sisvac.vaccine.application", "appointment_id", string="Vaccine Applications"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    product_id = fields.Many2one("product.product", string="Vaccine", required=True)
    location_id = fields.Many2one(
        "stock.location", string="Vaccination Center", required=True, check_company=True
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )


# class CalendarEvent(models.Model):
#     _inherit = "calendar.event"
#
#     appointment_number = fields.Char(readonly=True, default="New")
#     patient_id = fields.Many2one("res.partner")
#     next_appointment_date = fields.Datetime(readonly=True)
#     vaccination_appointment = fields.Boolean(readonly=True)
#     state = fields.Selection(
#         [("pending", "Pending"), ("done", "Done"), ("canceled", "Canceled")],
#         default="pending",
#         readonly=True,
#     )
#     dose_number = fields.Integer(readonly=True)
#     another_appointment_needed = fields.Boolean(readonly=True)
#     lots = fields.Char(readonly=True)
#     vaccinator_id = fields.Many2one(
#         "res.partner", readonly=True, domain=[("is_vaccinator", "=", True)]
#     )
#     patient_sign = fields.Binary(readonly=True)
#     got_symptoms = fields.Boolean("Got Symptoms?", readonly=True)
#     symptoms = fields.Text(readonly=True)
#
#     # Related
#     patient_image = fields.Binary("Patient photo", related="patient_id.image_1024")
#     patient_vat = fields.Char(related="patient_id.vat")
#
#     def _get_appointment_data(self):
#         return {
#             "appointment_number": self.appointment_number,
#             "patient_id": {"id": self.patient_id.id, "name": self.patient_id.name},
#             "next_appointment_date": self.next_appointment_date,
#             "state": self.state,
#             "dose_number": self.dose_number,
#             "another_appointment_needed": self.another_appointment_needed,
#             "lots": self.lots,
#             "vaccinator_id": {
#                 "id": self.vaccinator_id.id,
#                 "name": self.vaccinator_id.name,
#             },
#             "symptoms": self.symptoms,
#             "patient_vat": self.patient_vat,
#         }
#
#     @api.model
#     def create(self, vals):
#         if vals.get("appointment_number", "New") == "New":
#             vals["appointment_number"] = (
#                 self.env["ir.sequence"].next_by_code("sisvac.appointment") or "/"
#             )
#             vals["name"] = vals["appointment_number"]
#         return super(CalendarEvent, self).create(vals)
#
#     @api.constrains("patient_id", "status", "vaccination_appointment")
#     def _check_sigle_active_appointment(self):
#         for record in self:
#             appointment_filter = [
#                 ("vaccination_appointment", "=", True),
#                 ("state", "=", "pending"),
#                 ("patient_id", "=", record.patient_id.id),
#             ]
#
#             current_appointments = self.search_count(appointment_filter)
#
#             if current_appointments > 1:
#                 raise ValidationError(
#                     _(
#                         "This patient have another active vaccination appointment. \
#                     \nEach patient only can have one active vaccination appointment."
#                     )
#                 )
#
#     def action_put_vaccine(self):
#
#         return {
#             "name": _("Put Vaccine"),
#             "type": "ir.actions.act_window",
#             "view_type": "form",
#             "view_mode": "form",
#             "res_model": "sisvac.vaccination.wizard",
#             "target": "new",
#         }
