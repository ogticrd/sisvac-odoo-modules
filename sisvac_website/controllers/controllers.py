import json
import requests
from werkzeug.utils import redirect

from odoo import http
from odoo.http import request


class Vaccination(http.Controller):

    @http.route('/registry', type='http', auth='public', methods=['GET'], website=True)
    def website_appointment(self, **kwargs):
        dr_country_id = 61
        country_states = request.env['res.country.state'].search([("country_id", "=", dr_country_id)])

        return request.render(
            'sisvac_website.sisvac_vaccination_website_form',
            {"country_states": country_states}
        )

    @http.route('/sisvac/patient_api/<vat>', auth='none', cors="*")
    def get_patient_name(self, vat):

        patient_display_name = self._get_patient_data(vat).get("name", False)
        if not patient_display_name:
            return {"message": "An error has been occurred"}

        patient_name = patient_display_name.split(" ")[0]

        return json.dumps({"patient_name": patient_name})

    @http.route('/sisvac/update_patient/', type="http", auth='public', csrf=False, method='POST', website=True)
    def update_patient_kk(self, **post):
        if len(post) <= 0:
            return

        partner_data = {}
        partner_allow_data = [
            "phone", "mobile", "state_id", "city", "email", "street",
            "sisvac_has_hypertension", "sisvac_has_diabetes", "sisvac_has_obesity",
            "sisvac_has_asthma", "sisvac_has_cardiovascular", "sisvac_has_renal_insufficiency",
            "sisvac_has_discapacity", "sisvac_health_notes",
            "sisvac_emergency_contact_name", "sisvac_emergency_contact_vat",
            "sisvac_emergency_contact_phone", "sisvac_emergency_contact_relationship"
        ]
        partner = request.env["res.partner"].sudo().search([("vat", "=", post.get("vat"))], limit=1)

        for f, v in post.items():
            if v and f in partner_allow_data:
                partner_data.update({f: v})

        if partner_data:
            partner_data.update({"country_id": 61, "sisvac_pre_registered": True})

            if partner:
                partner.sudo().update(partner_data)
            else:
                patient_vat = post.get("vat")
                patient_name = self._get_patient_data(patient_vat).get("name")
                partner_data.update({"vat": patient_vat, "name": patient_name})
                request.env["res.partner"].sudo().create(partner_data)

        return redirect("/contactus-thank-you")

    def _get_patient_data(self, vat):
        patient_api = "https://citizens.api.digital.gob.do/api/citizens/basic-data?key=AIzaSyBrjBWquMuEZ1nUZd4-O5cwNVzOOitiqls=&id="

        try:
            req = requests.get(patient_api + str(vat))
            if req.status_code != requests.codes.ok:
                return {"message": "The request has the following status code: " + req.status_code}
        except requests.exceptions.ConnectionError as e:
            return {"message": "The request has the following error message: " + str(e)}
        except requests.exceptions.Timeout as e:
            return {"message": "The request has the following error message: " + str(e)}

        return req.json()
