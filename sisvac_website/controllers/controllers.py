import json
import requests
from werkzeug.utils import redirect

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

    @http.route('/sisvac/patient_api/<int:vat>', auth='none', cors="*")
    def get_patient(self, vat):
        patient_api = "https://citizens-api.digital.gob.do/api/citizens/basic-data?id="

        try:
            req = requests.get(patient_api + str(vat))
            if req.status_code != requests.codes.ok:
                return False
        except requests.exceptions.ConnectionError as e:
            return False
        except requests.exceptions.Timeout as e:
            return False

        content = req.json()
        patient_name = content.get("name").split(" ")[0]

        return json.dumps({"patient_name": patient_name})

    @http.route('/sisvac/update_patient/', type="http", auth='public', csrf=False, method='POST', website=True)
    def update_patient_kk(self, **post):
        if len(post) <= 0:
            return

        partner_data = {}
        partner_allow_data = ["phone", "mobile", "state_id", "city", "email", "disability", "notes"]
        partner = request.env["res.partner"].sudo().search([("vat", "=", post.get("vat"))], limit=1)
        if not partner:
            return

        for f, v in post.items():
            if v and v in partner_allow_data:
                partner_data.update({f: v})

        if partner_data:
            partner_data.update({"country_id": 61})
            partner.sudo().update(partner_data)

        return redirect("/contactus-thank-you")