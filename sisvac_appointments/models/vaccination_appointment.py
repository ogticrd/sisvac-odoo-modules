from odoo import fields, models, api
from odoo.exceptions import UserError


class VaccineApplication(models.Model):
    _name = "sisvac.vaccine.application"
    _description = "Vaccine Application"
    _order = "application_date"
    _inherits = {"calendar.event": "event_id"}

    event_id = fields.Many2one(
        "calendar.event", string="Event", required=True, ondelete="cascade"
    )
    appointment_id = fields.Many2one(
        "sisvac.vaccination.appointment",
        string="Appointment",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one("res.partner", string="Patient", required=True)
    medic_partner_id = fields.Many2one(
        "res.partner",
        string="Vaccinator",
        domain="[('sisvac_is_vaccinator', '=', True)]",
    )
    application_date = fields.Datetime()
    state = fields.Selection(
        [("draft", "Draft"), ("scheduled", "Scheduled"), ("applied", "Applied")],
        default="draft",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Vaccine",
        store=True,
        readonly=True,
    )
    lot_id = fields.Many2one(
        "stock.production.lot",
        string="Lot",
        domain="[('product_id', '=', product_id)]",
        check_company=True,
    )
    symptom_ids = fields.Many2many("sisvac.symptom")
    symptom_notes = fields.Text()
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    @api.model
    def create(self, vals):
        if "appointment_id" in vals:
            appointment = self.env["sisvac.vaccination.appointment"].browse(
                vals["appointment_id"]
            )
            vals["name"] = appointment.name
            vals["start"] = vals["application_date"]
            vals["stop"] = vals["application_date"]

        return super(VaccineApplication, self).create(vals)

    def apply(self):
        self.write(
            {
                "medic_partner_id": self.medic_partner_id.id,
                "application_date": self.application_date,
                "lot_id": self.lot_id.id,
                "state": "applied",
            }
        )

        application_id = self.search(
            [
                ("state", "=", "scheduled"),
                ("appointment_id", "=", self.appointment_id.id),
            ],
            order="application_date desc",
            limit=1,
        )

        self.appointment_id.write(
            {
                "last_appointment_date": self.application_date,
                "next_appointment_date": application_id.application_date
                if application_id
                else False,
                "state": "completed" if not application_id else application_id.state,
            }
        )

    def _get_application_data(self):
        return {
            "id": self.id,
            "cedula": self.partner_id.vat,
            "vaccine": {"id": self.product_id.id, "name": self.product_id.name},
            "lot": {"id": self.lot_id.id, "name": self.lot_id.name},
            "location": {
                "id": self.appointment_id.location_id.id,
                "name": self.appointment_id.location_id.name,
            },
            "date": fields.Date.to_string(self.application_date.date())
            if self.application_date
            else False,
            "hour": self.application_date.hour if self.application_date else False,
            "next_date": fields.Date.to_string(
                self.appointment_id.next_appointment_date.date()
            )
            if self.appointment_id.next_appointment_date
            else False,
            "symptoms": [{"id": s.id, "name": s.name} for s in self.symptom_ids]
        }


class VaccinationAppointment(models.Model):
    _name = "sisvac.vaccination.appointment"
    _description = "Vaccination Appointment"
    _inherit = "mail.thread"
    _order = "next_appointment_date, name"

    name = fields.Char(
        string="Appointment Number",
        required=True,
        readonly=True,
        default="Draft",
        copy=False,
    )

    # Patient
    partner_id = fields.Many2one(
        "res.partner",
        domain="[('sisvac_is_patient', '=', True)]",
        string="Name",
        required=True,
    )
    patient_signature = fields.Binary()  # TODO: implement this stuff
    image_1920 = fields.Binary(related="partner_id.image_1920")
    birthdate_date = fields.Date(related="partner_id.birthdate_date")
    age = fields.Integer(related="partner_id.age")
    gender = fields.Selection(related="partner_id.gender")
    age_range_id = fields.Many2one(
        "res.partner.age.range", related="partner_id.age_range_id"
    )
    observations = fields.Text(copy=False)

    # Appointment
    first_appointment_date = fields.Datetime(
        required=True, states={"draft": [("required", False)]}
    )
    last_appointment_date = fields.Datetime(readonly=True, copy=False)
    next_appointment_date = fields.Datetime(readonly=True, copy=False)
    application_ids = fields.One2many(
        "sisvac.vaccine.application",
        "appointment_id",
        string="Vaccine Applications",
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
        copy=False,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Vaccine",
        domain="[('sisvac_is_vaccine', '=', True)]",
        required=True,
    )
    location_id = fields.Many2one(
        "stock.location",
        string="Vaccination Center",
        check_company=True,
        required=True,
    )
    show_vaccine_wizard_button = fields.Boolean(
        compute="_compute_show_vaccine_wizard_button",
        store=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    @api.depends("state")
    def _compute_show_vaccine_wizard_button(self):
        for apt in self:
            apt.show_vaccine_wizard_button = bool(
                apt.application_ids.filtered(lambda app: app.state == "scheduled")
            )

    def _get_next_appointment_date(self, start_date, interval, time_unit):
        if time_unit in ("days", "weeks"):
            return fields.Datetime.add(
                start_date, days=interval * 7 if time_unit == "weeks" else interval
            )
        elif time_unit == "months":
            return fields.Datetime.add(start_date, months=interval)
        else:
            return fields.Datetime.add(start_date, years=interval)

    def action_confirm_appointment(self):

        date_range = []
        for i in range(self.product_id.sisvac_dose_interval):
            date = self.first_appointment_date if i == 0 else date_range[-1]
            date_range.append(
                self._get_next_appointment_date(
                    date,
                    self.product_id.sisvac_dose_interval,
                    self.product_id.sisvac_unit_time_between_dose,
                )
            )

        if not date_range:
            raise UserError("%s vaccine has no dose interval" % self.product_id.name)

        seq_code = "sisvac.appointment"
        self.write(
            {
                "state": "scheduled",
                "name": self.env["ir.sequence"].sudo().next_by_code(seq_code),
                "next_appointment_date": date_range[0],
                "application_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": self.partner_id.id,
                            "application_date": date,
                            "state": "scheduled",
                            "product_id": self.product_id.id,
                        },
                    )
                    for date in date_range
                ],
            }
        )

    def action_apply_vaccine_wizard(self):
        application_id = self.env["sisvac.vaccine.application"].search(
            [("state", "=", "scheduled"), ("appointment_id", "=", self.id)],
            order="application_date desc",
            limit=1,
        )
        if not application_id:
            raise UserError("Not pending vaccine application found.")

        view_id = self.env.ref(
            "sisvac_appointments.sisvac_vaccine_application_wizard_view"
        ).id

        return {
            "type": "ir.actions.act_window",
            "name": "Apply Vaccine",
            "res_model": "sisvac.vaccine.application",
            "view_mode": "form",
            "res_id": application_id.id,
            "views": [(view_id, "form")],
            "target": "new",
        }

    def _get_appointment_data(self):
        return {
            "id": self.id,
            "number": self.name,
            "state": self.state,
            "cedula": self.partner_id.vat,
            "name": self.partner_id.name,
            "date": fields.Date.to_string(self.next_appointment_date.date())
            if self.next_appointment_date
            else False,
            "hour": self.next_appointment_date.hour
            if self.next_appointment_date
            else False,
            "location": {
                "id": self.location_id.id,
                "name": self.location_id.name,
            },
            "dose": len(
                self.application_ids.filtered(lambda ap: ap.state == "applied")
            ),
        }
