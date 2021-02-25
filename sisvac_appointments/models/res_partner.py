from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    sisvac_is_vaccinator = fields.Boolean("Is Vaccinator")
    sisvac_is_patient = fields.Boolean("Is Patient")
    sisvac_is_vaccination_center = fields.Boolean("Is Vaccination Center")

    @api.constrains(
        "sisvac_is_vaccinator", "sisvac_is_patient", "sisvac_is_vaccination_center"
    )
    def _check_sisvac_is_vaccination_center(self):
        for partner in self.filtered(lambda p: p.sisvac_is_vaccination_center):
            if partner.sisvac_is_vaccinator or partner.sisvac_is_patient:
                raise ValidationError(
                    _("Vaccination Center can't be set as Patient/Vaccinator")
                )
