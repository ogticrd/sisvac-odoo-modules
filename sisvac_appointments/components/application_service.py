import json
from odoo import fields
from odoo.http import request, Response
from odoo.addons.component.core import Component


class ApplicationService(Component):
    _inherit = "base.rest.service"
    _name = "application.service"
    _usage = "application"
    _collection = "sisvac.services"
    _description = """
        Vaccines Application Related models API Services
    """

    def get(self, _id):
        application = self.env["sisvac.vaccine.application"].browse(_id)
        return request.make_response(
            json.dumps(application._get_application_data()),
            headers=[("Content-Type", "application/json")],
        )

    def search(self):
        params = self.work.request.params
        application_obj = self.env["sisvac.vaccine.application"]
        if "limit" in params:
            applications = application_obj.search([], limit=int(params["limit"]))
        else:
            applications = application_obj.search([])
        return request.make_response(
            json.dumps([app._get_application_data() for app in applications]),
            headers=[("Content-Type", "application/json")],
        )

    def _parse_date(self, params):

        try:
            date_string = params["date"] + " " + params["hour"]
            date = fields.Datetime.from_string(date_string)
        except ValueError:
            return Response(
                "Error. Time data %s %s does not match format 'Y-m-d H:M:S'"
                % (params["date"], params["hour"]),
                status="400",
            )
        return date

    def create(self):
        params = self.work.request.params

        required_fields = [
            "cedula",
            "name",
            "vaccine",
            "vaccinator",
            "lot",
            "location",
            "date",
            "hour",
            "dose",
        ]
        missing_fields = [f for f in required_fields if f not in params]

        if missing_fields:
            return Response(
                "Error. %s params required for application create"
                % ", ".join(missing_fields),
                status="400",
            )

        vat = params["cedula"]
        Partner = self.env["res.partner"]
        partner_id = Partner.search([("vat", "=", vat)], limit=1)
        if not partner_id:
            partner_id = Partner.create(
                {"name": params.get("name"), "vat": vat, "sisvac_is_patient": True}
            )

        vaccinator_id = Partner.browse(int(params["vaccinator"]))
        if not vaccinator_id:
            return Response("Error. Vaccinator not found.", status="400")

        lot_id = self.env["stock.production.lot"].browse(int(params["lot"]))
        if not lot_id:
            return Response("Error. Lot not found.", status="400")

        product = params["vaccine"]
        product_id = self.env["product.product"].browse(int(product))
        if not product_id:
            return Response("Error. Vaccine not found.", status="400")

        location = params["location"]
        location_id = self.env["stock.location"].browse(int(location))
        if not location_id:
            return Response("Error. Location not found.", status="400")

        Appointment = self.env["sisvac.vaccination.appointment"]
        appointment_id = Appointment.search(
            [
                ("state", "not in", ("completed", "cancelled")),
                ("partner_id", "=", partner_id.id),
                ("product_id", "=", product_id.id),
            ],
            limit=1,
        )

        date = self._parse_date(params)

        if not appointment_id:
            appointment_id = Appointment.create(
                {
                    "partner_id": partner_id.id,
                    "first_appointment_date": date,
                    "product_id": product_id.id,
                    "location_id": location_id.id,
                }
            )
            appointment_id.with_context(
                dose=params["dose"],
                date=date,
                vaccinator=params["vaccinator"],
                lot=params["lot"],
            ).action_confirm_appointment()

        else:
            application_id = self.env["sisvac.vaccine.application"].search(
                [
                    ("appointment_id", "=", appointment_id.id),
                    ("state", "=", "scheduled"),
                ],
                order="application_date asc",
                limit=1
            )
            if not application_id:
                return Response(
                    "Error. No pending applications found for given dose.", status="400"
                )

            application_id.update(
                {
                    "application_date": date,
                    "state": "applied",
                    "medic_partner_id": int(params["vaccinator"]),
                    "lot_id": int(params["lot"]),
                }
            )
            application_id.apply()
