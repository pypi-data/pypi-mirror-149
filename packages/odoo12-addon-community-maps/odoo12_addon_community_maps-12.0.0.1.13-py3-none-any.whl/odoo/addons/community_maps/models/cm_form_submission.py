import json
import re
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
from odoo.addons.community_maps.models.cm_utils import CmUtils

class CmFormSubmission(models.Model):
  # _name = 'cm.form.submission'
  _inherit = 'crm.lead'

  team_type = fields.Char(string=_("Team type"),compute="_get_team_type",store=False)
  submission_type = fields.Selection([('place_submission',_("Place submission")),('place_proposal_submission',_("Place proposal"))],string=_("Submission type (maps)"))
  # name = fields.Char(string=_("Name"))
  form_submission_metadata_ids = fields.One2many('cm.form.submission.metadata',
    'submission_id',string=_("Submission metadata"))
  crowdfunding_type = fields.Selection(
    selection=CmUtils.get_system_crowdfunding_types_selection(),
    default='none',
    compute="_get_crowdfunding_type",
    string=_("Crowdfunding type"),
    store=False)
  shareable_url = fields.Char(_("Shareable url"))

  _order = "id desc"

  _sql_constraints = [
    ('check_probability', 'check(probability >= 0)', 'The probability of closing the deal should be bigger than 0%')
  ]

  @api.multi
  def unlink(self):
    for record in self:
      related_proposal_teams = self.env['crm.team'].search([('proposal_form_submission_id','=',record.id)])
      if record.team_id or related_proposal_teams.exists():
        raise ValidationError(_("You can't delete. Some Teams relate on this info. Archive instead."))
      return super(CmFormSubmission, record).unlink()

  @api.depends('team_id')
  def _get_crowdfunding_type(self):
    for record in self:
      try:
        crowdfunding_type = record.team_id.map_id.crowdfunding_type
      except:
        crowdfunding_type = False
      record.crowdfunding_type = crowdfunding_type 

  @api.depends('team_id')
  def _get_team_type(self):
    for record in self:
      try:
        team_type = record.team_id.team_type
      except:
        team_type = False
      record.team_type = team_type

  @api.constrains('planned_revenue')
  def constrain_revenue(self):
    for record in self:
      if record.team_id:
        record.team_id._get_total_committed_invoicing()
        record.team_id._get_completed_percentage()
      record.recompute_probability()
      self._crowdfunding_notify_if_must()

  @api.constrains('team_id')
  def contrain_team_id(self):
    for record in self:
      record.recompute_probability()
    self._crowdfunding_notify_if_must()

  def recompute_probability(self):
    if self.team_id:
      for submission in self.team_id.form_submission_ids:
        submission.update_probability()
    else:
      submissions = self.env['crm.lead'].search([('team_type','=','map_place')])
      if submissions.exists():
        for submission in submissions:
          submission.update_probability()
    self.update_probability()#TODO: check if this line needed

  def update_probability(self):
    probability = 0
    if self.team_id:
      probability = self.team_id.completed_percentage
    self.write({
      'probability': probability
    })

  def _crowdfunding_notify_if_must(self):
    if self.team_id:
      self.team_id.crowdfunding_notify_if_must()

  def create_submission_metadata(self,data,fields_map=False):
    model_update_dict = {}
    for key in data:
      if key != 'address':
        # metadata
        metadata = {
          'key': key,
          'value': str(data[key]),
          'submission_id': self.id
        }
        # model map
        if fields_map:
          jfields_map = json.loads(fields_map)
          if key in jfields_map.keys():
            if jfields_map[key]['type'] == 'number':
              value = float(data[key])
            elif jfields_map[key]['type'] == 'number_in_cents':
              value = float(data[key])/100
            elif jfields_map[key]['type'] == 'currency_text':
              value = [float(s) for s in re.findall(r'-?\d+\.?\d*', data[key])][0]
            else:#string
              value = str(data[key])
            model_update_dict[jfields_map[key]['model_field']] = value
            metadata['mapped_to'] = "submission." + jfields_map[key]['model_field']
        # write metadata
        metadata = self.env['cm.form.submission.metadata'].create(metadata)
    if model_update_dict:
      self.write(model_update_dict)
