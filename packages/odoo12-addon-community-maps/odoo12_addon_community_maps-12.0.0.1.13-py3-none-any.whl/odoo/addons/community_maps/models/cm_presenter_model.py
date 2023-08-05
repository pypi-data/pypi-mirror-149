from odoo import models, api, fields
from odoo.tools.translate import _

class CmPresenterModel(models.Model):
  _name = 'cm.presenter.model'

  name = fields.Char(string=_("Name"))

  allowed_in_map_mids = fields.Many2many('cm.map', 'cm_maps_presenter_models', 'presenter_model_id', 'map_id',
    string=_("Allowed in maps"))

  json_dataschema = fields.Text(string=_("Schema Data"))
  json_schema = fields.Text(string=_("Schema"))
  json_uischema = fields.Text(string=_("UiSchema"))