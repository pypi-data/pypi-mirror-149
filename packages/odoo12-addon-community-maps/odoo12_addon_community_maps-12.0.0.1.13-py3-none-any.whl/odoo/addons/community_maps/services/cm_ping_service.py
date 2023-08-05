from marshmallow import fields

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.addons.datamodel.core import Datamodel

class PingMessage(Datamodel):
    _name = "ping.message"

    message = fields.String(required=True, allow_none=False)


class PingService(Component):
    _inherit = 'base.rest.private_abstract_service'
    _name = 'ping.service'
    _usage = 'ping'
    _description = """
      Ping Service
    """


    @restapi.method(
        [(["/pong"], "GET")],
        input_param=restapi.Datamodel("ping.message"),
        output_param=restapi.Datamodel("ping.message"),
        auth="public",
    )
    def pong(self, ping_message):
        PingMessage = self.env.datamodels["ping.message"]
        return_data = PingMessage(message = "Received: " + ping_message.message)
        return return_data