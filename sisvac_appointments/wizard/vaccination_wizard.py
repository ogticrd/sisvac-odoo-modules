from odoo import fields, models, api, _


class Vaccination(models.TransientModel):
    _name = "sisvac.vaccination.wizard"
    _description = "Vaccination Wizard"

    lots = fields.Char()
    vaccinator_id = fields.Many2one(
        "res.partner", domain=[("is_vaccinator", "=", True)]
    )
    got_symptoms = fields.Boolean("Got Symptoms?")
    symptom_notes = fields.Text()
    symptom_ids = fields.Many2many("sisvac.symptom")

    def _get_vaccination_data(self):
        """Hook method to be extended on other modules"""
        return {
            "lots": self.lots,
            "vaccinator_id": self.vaccinator_id.id,
            "got_symptoms": self.got_symptoms,
            "symptoms": self.symptoms,
            "state": "done",
        }

    def put_vaccine(self):
        self.ensure_one()
        active_id = self._context.get("active_id")
        appointment = self.env["calendar.event"].browse(active_id)
        appointment.write(self._get_vaccination_data())
