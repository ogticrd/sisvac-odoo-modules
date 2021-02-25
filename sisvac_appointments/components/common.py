import json
from odoo import models
from odoo.http import Response


class SisvacComponentsCommon(models.AbstractModel):
    _name = "sisvac.components.common"
    _description = "SISVAC Components Common"

    @staticmethod
    def response_wrapper(success, status, data=None, message="", headers=None):

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
