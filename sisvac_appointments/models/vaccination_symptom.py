from odoo import fields, models


class Symptom(models.Model):
    _name = "sisvac.symptom"
    _description = "Symptoms"

    name = fields.Char(required="True")
