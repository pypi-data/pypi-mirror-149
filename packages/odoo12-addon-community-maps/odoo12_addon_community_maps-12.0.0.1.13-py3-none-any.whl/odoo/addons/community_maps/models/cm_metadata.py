from odoo import models, api, fields
from odoo.tools.translate import _

class CMetadata(models.Model):
  _name = 'cm.metadata'

  type = fields.Char(string=_("Type"))
  format = fields.Char(string=_("Format"))
  key = fields.Char(string=_("Key"))
  value = fields.Char(string=_("Value"))
  sort_order = fields.Integer(string=_("Sort order"))

  _order = "sort_order asc"