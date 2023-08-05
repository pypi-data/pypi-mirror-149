from odoo import models, api, fields
from odoo.tools.translate import _

class CmPlaceCrowdfundingNotificationRequest(models.Model):
  _name = 'cm.crowdfunding.notification.request'

  map_id = fields.Many2one('crm.map',string=_("Map"),ondelete='cascade')
  percentage = fields.Integer(string=_("Percentage"))

  _order = "percentage desc"