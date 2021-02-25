from odoo.addons.component.core import Component

from .common import SisvacComponentsCommon

ResponseWrapper = SisvacComponentsCommon.response_wrapper


class ConsentService(Component):
    _inherit = "base.rest.service"
    _name = "consent.service"
    _usage = "consents"
    _collection = "sisvac.services"
    _description = """
        Consent Related models API Services
    """

    def get(self, _id):
        consent = self.env["sisvac.vaccination.consent"].browse(_id)
        return ResponseWrapper(
            success=True,
            status=200,
            data=consent._get_consent_data(),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        consent_obj = self.env["sisvac.vaccination.consent"]
        if "limit" in params:
            consents = consent_obj.search([], limit=int(params["limit"]))
        else:
            consents = consent_obj.search([])
        return ResponseWrapper(
            success=True,
            status=200,
            data=[c._get_consent_data() for c in consents],
            headers=[("Content-Type", "application/json")],
        )

    def create(self):
        params = self.work.request.params
        if "cedula" not in params:
            return ResponseWrapper(
                success=False,
                status=400,
                message="cedula param is required for consent create",
                headers=[("Content-Type", "application/json")],
            )

        Partner = self.env["res.partner"]
        vat = params["cedula"]
        partner_id = Partner.search([("vat", "=", vat)], limit=1)
        if not partner_id:
            partner_id = Partner.create({"name": params.get("name"), "vat": vat})

        consent_id = self.env["sisvac.vaccination.consent"].create(
            {
                "partner_id": partner_id.id,
                "patient_signature": params.get("patient_signature", False)
                if params.get("patient_signature", False) == "true"
                else False,
                "has_covid": params.get("has_covid", False)
                if params.get("has_covid", False) == "true"
                else False,
                "is_pregnant": params.get("is_pregnant", False)
                if params.get("is_pregnant", False) == "true"
                else False,
                "had_fever": params.get("had_fever", False)
                if params.get("had_fever", False) == "true"
                else False,
                "is_vaccinated": params.get("is_vaccinated", False)
                if params.get("is_vaccinated", False) == "true"
                else False,
                "had_reactions": params.get("had_reactions", False)
                if params.get("had_reactions", False) == "true"
                else False,
                "is_allergic": params.get("is_allergic", False)
                if params.get("is_allergic", False) == "true"
                else False,
                "is_medicated": params.get("is_medicated", False)
                if params.get("is_medicated", False) == "true"
                else False,
                "had_transplants": params.get("had_transplants", False)
                if params.get("had_transplants", False) == "true"
                else False,
            }
        )

        return ResponseWrapper(
            success=True,
            status=200,
            data=consent_id._get_consent_data(),
            headers=[("Content-Type", "application/json")],
        )
