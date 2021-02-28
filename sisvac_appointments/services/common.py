import json
from odoo import api
from odoo.http import Response
from odoo.addons.component.core import Component


class SisvacComponentsCommon(Component):
    _name = "sisvac.components.common"
    _description = "SISVAC Components Common"

    @api.model
    def response_wrapper(self, success, status, data=None, message="", headers=None):

        return Response(
            json.dumps(
                {
                    "success": success,
                    "status": status,
                    "data": data,
                    "message": message,
                }
            ),
            status=status,
            headers=headers,
        )
