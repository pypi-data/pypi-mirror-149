from odoo import models, api, fields
from odoo.tools.translate import _

class CmPlacePresenterMetadata(models.Model):
  _name = 'cm.place.presenter.metadata'
  _inherit = 'cm.metadata'

  place_id = fields.Many2one('crm.team',string=_("Place"),ondelete='cascade')