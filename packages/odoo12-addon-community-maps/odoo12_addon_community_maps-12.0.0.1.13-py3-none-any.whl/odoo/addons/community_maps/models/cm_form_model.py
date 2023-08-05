import json
from odoo import models, api, fields
from odoo.tools.translate import _

class CmFormModel(models.Model):
  _name = 'cm.form.model'

  _inherit = ["cm.slug.id.mixin"]

  name = fields.Char(string=_("Name"))
  description = fields.Char(string=_("Description"))
  cta_label = fields.Char(string=_("Open form, presenter button label"))
  button_label = fields.Char(string=_("Button Label"))
  submission_ok_message = fields.Text(string=_("Successful message"))
  submission_ok_email_template_id = fields.Many2one('mail.template',
    string=_("Successful email template"))
  follower_partner_id = fields.Many2one('res.partner',
    string=_("Partner to be notified on form submission"))
  generate_submission_in_proposal = fields.Boolean(
    string=_("Create a crowdfunding submission if form used as proposal"))

  allowed_in_map_mids = fields.Many2many('cm.map', 'cm_maps_form_models', 'form_model_id', 'map_id',
    string=_("Allowed in maps"))

  json_initial_data = fields.Text(string=_("Initial Data"))
  json_schema = fields.Text(string=_("Schema"))
  json_uischema = fields.Text(string=_("UiSchema"))
  json_submission_fields_map = fields.Text(string=_("Submission fields map"))
  json_place_proposal_submission_fields_map = fields.Text(string=_("Place proposal submission fields map"))
  json_place_proposal_fields_map = fields.Text(string=_("Place proposal fields map"))

  def get_datamodel_dict(self,submission_form=True):
    datamodel = {
      'slug': self.slug_id,
      'formButtonLabel': self.button_label,
      'description': None,
      'initialData': json.loads(self.json_initial_data),
      'jsonSchema': json.loads(self.json_schema),
      'uiSchema': json.loads(self.json_uischema),
    }
    if submission_form:
      datamodel['ctaLabel'] = self.cta_label
    if self.description:
      datamodel['description'] = self.description
    return datamodel