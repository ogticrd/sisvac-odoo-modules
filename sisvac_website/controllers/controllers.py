from odoo import http
from odoo.http import request


class Vaccination(http.Controller):

    @http.route('/appointment', type='http', auth='public', methods=['GET'], website=True)
    def website_appointment(self, **kwargs):
        dr_country_id = 61
        country_states = request.env['res.country.state'].search([("country_id", "=", dr_country_id)])

        return request.render(
            'sisvac_website.sisvac_vaccination_website_form',
            {"country_states": country_states}
        )
