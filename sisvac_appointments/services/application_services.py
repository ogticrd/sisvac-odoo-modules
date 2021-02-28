from odoo import fields
from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class ApplicationService(Component):
    _inherit = ["base.rest.service", "sisvac.components.common"]
    _name = "application.service"
    _usage = "application"
    _collection = "sisvac.services"
    _description = """
        Vaccines Application Related models API Services
    """

    def get(self, _id):
        application = self.env["sisvac.vaccine.application"].browse(_id)
        return self.response_wrapper(
            success=True,
            status=200,
            data=application._get_application_data(),
            headers=[("Content-Type", "application/json")],
        )

    def search(self, limit):
        application_obj = self.env["sisvac.vaccine.application"]

        if not limit:
            applications = application_obj.search([])
        else:
            applications = application_obj.search([], limit=limit)

        return self.response_wrapper(
            success=True,
            status=200,
            data=[app._get_application_data() for app in applications],
            headers=[("Content-Type", "application/json")],
        )

    def _validator_search(self):
        return {
            "limit": {
                "type": "integer",
                "coerce": to_int,
            }
        }

    def _parse_date(self, params):

        try:
            date_string = params["date"] + " " + params["hour"]
            date = fields.Datetime.from_string(date_string)
        except ValueError:
            return self.response_wrapper(
                success=False,
                status=400,
                headers=[("Content-Type", "application/json")],
                message="Time data %s %s does not match format 'Y-m-d H:M:S'"
                % (params["date"], params["hour"]),
            )
        return date

    def create(self, **params):

        vat = params["cedula"]
        Partner = self.env["res.partner"]
        partner_id = Partner.search([("vat", "=", vat)], limit=1)
        if not partner_id:
            partner_id = Partner.create(
                {"name": params.get("name"), "vat": vat, "sisvac_is_patient": True}
            )

        vaccinator_id = Partner.browse(int(params["vaccinator"]))
        if not vaccinator_id:
            return self.response_wrapper(
                success=False,
                status=400,
                headers=[("Content-Type", "application/json")],
                message="Vaccinator not found",
            )

        lot_id = self.env["stock.production.lot"].browse(int(params["lot"]))
        if not lot_id:
            return self.response_wrapper(
                success=False,
                status=400,
                headers=[("Content-Type", "application/json")],
                message="Lot not found",
            )

        product = params["vaccine"]
        product_id = self.env["product.product"].browse(int(product))
        if not product_id:
            return self.response_wrapper(
                success=False,
                status=400,
                headers=[("Content-Type", "application/json")],
                message="Vaccine not found",
            )

        location = params["location"]
        location_id = self.env["stock.location"].browse(int(location))
        if not location_id:
            return self.response_wrapper(
                success=False,
                status=400,
                headers=[("Content-Type", "application/json")],
                message="Location not found",
            )

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
                limit=1,
            )
            if not application_id:
                return self.response_wrapper(
                    success=False,
                    status=400,
                    headers=[("Content-Type", "application/json")],
                    message="No pending applications found for given dose",
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

            return self.response_wrapper(
                success=True,
                status=200,
                headers=[("Content-Type", "application/json")],
                message="Appointment %s Vaccine Application update"
                % appointment_id.name,
            )

    def _validator_create(self):
        return {
            "cedula": {"type": "string", "required": True},
            "name": {"type": "string", "required": True},
            "vaccine": {"type": "integer", "required": True, "coerce": to_int},
            "vaccinator": {
                "type": "integer",
                "required": True,
                "coerce": to_int,
            },
            "lot": {"type": "integer", "required": True, "coerce": to_int},
            "location": {"type": "integer", "required": True, "coerce": to_int},
            "date": {"type": "string", "required": True},
            "hour": {"type": "string", "required": True},
            "dose": {"type": "integer", "required": True, "coerce": to_int},
        }
