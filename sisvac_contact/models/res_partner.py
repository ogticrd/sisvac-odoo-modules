from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    sisvac_has_hypertension = fields.Boolean("Has Hypertension")
    sisvac_has_diabetes = fields.Boolean("Has Diabetes")
    sisvac_has_obesity = fields.Boolean("Has Obesity")
    sisvac_has_asthma = fields.Boolean("Has Asthma")
    sisvac_has_cardiovascular = fields.Boolean("Has Cardiovascular")
    sisvac_has_renal_insufficiency = fields.Boolean("Has Renal Insufficiency")
    sisvac_has_discapacity = fields.Boolean("Has Discapacity")
    sisvac_health_notes = fields.Boolean("Health Notes")
    sisvac_emergency_contact_name = fields.Char("Emergency Contact Name")
    sisvac_emergency_contact_vat = fields.Char("Emergency Contact Vat")
    sisvac_emergency_contact_phone = fields.Char("Emergency Contact Phone")
    sisvac_emergency_contact_relationship = fields.Selection(
        [
            ("Abuelo/Abuela", "Abuelo/Abuela"),
            ("Padre/Madre", "Padre/Madre"),
            ("Tio/Tia", "Tio/Tia"),
            ("Esposo/Esposa", "Esposo/Esposa"),
            ("Suegro/Suegra", "Suegro/Suegra"),
            ("Hermano/Hermana", "Hermano/Hermana"),
            ("Hijo/Hija", "Hijo/Hija"),
            ("Nieto/Nieta", "Nieto/Nieta"),
            ("Sobrino/Sobrina", "Sobrino/Sobrina"),
            ("Hijastro/Hijastra", "Hijastro/Hijastra")
        ], string="Emergency Contact Phone"
    )  # TODO: fix value names
    sisvac_pre_registered = fields.Boolean("Pre-registered")
