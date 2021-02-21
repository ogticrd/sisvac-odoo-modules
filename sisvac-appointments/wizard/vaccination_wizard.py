from odoo import fields, models, api, _


class Vaccination(models.TransientModel):
    _name = "sisvac.vaccination.wizard"
    _description = "Vaccination Wizard"

    product_id = fields.Many2one("product.template", "Vaccine", domain=[("is_vaccine", "=", True)])
    lots = fields.Char()
    vaccinator_id = fields.Many2one("res.partner", domain=[("is_vaccinator", "=", True)])
    got_symptoms = fields.Boolean("Got Symptoms?")
    symptoms = fields.Text()

    def put_vaccine(self):
        active_id = self._context.get('active_id')
        appointment = self.env['calendar.event'].browse(active_id)

        return appointment.write({
            'product_id': self.product_id,
            'lots': self.lots,
            'vaccinator_id': self.vaccinator_id,
            'got_symptoms': self.got_symptoms,
            'symptoms': self.symptoms,
            'state': 'done'
        })
