import json
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.addons.community_maps.models.cm_utils import CmUtils
from odoo.exceptions import ValidationError

class CmMap(models.Model):
  _name = 'cm.map'

  _inherit = ["cm.slug.id.mixin"]

  name = fields.Char(string=_("Name"))
  colorschema_id = fields.Many2one('cm.map.colorschema',string=_("Color schema"))
  proposal_form_model_id = fields.Many2one('cm.form.model',string=_("Proposal submission form"))
  allowed_form_model_mids = fields.Many2many('cm.form.model', 
    'cm_maps_form_models', 'map_id', 'form_model_id',string=_("Allowed forms"))
  allowed_place_category_mids = fields.Many2many('cm.place.category', 
    'cm_maps_place_categories', 'map_id', 'place_category_id',string=_("Allowed categories"))
  allowed_place_category_inproposal_mids = fields.Many2many('cm.place.category', 
    'cm_maps_place_categories_inpropsal', 'map_id', 'place_category_id',string=_("Allowed categories in proposal"))
  allowed_presenter_model_mids = fields.Many2many('cm.presenter.model', 
    'cm_maps_presenter_models', 'map_id', 'presenter_model_id',string=_("Allowed persenters"))
  place_ids = fields.One2many('crm.team','map_id',string=_("Places"))
  crowdfunding_type = fields.Selection(
    selection=CmUtils.get_system_crowdfunding_types_selection(),
    default='none', required=True, string=_("Crowdfunding type"))
  tile_style = fields.Char(string=_("Tile style"))
  show_progress_on_marker = fields.Boolean(string=_('Show progress on marker'))
  allow_filter_by_status = fields.Boolean(string=_('"Active" filter'))
  allow_filter_by_category = fields.Boolean(string=_('"Category" filter'))
  allow_filter_by_crowdfunding = fields.Boolean(string=_('"Crowdfunding" filter'))
  privacy_link = fields.Char(string=_("T&C: Privacy url"))
  cookies_link = fields.Char(string=_("T&C: Cookies url"))
  submission_ok_message = fields.Text(
    string=_("Successful message"),
    compute='_get_submission_ok_message',
    store=False)
  submission_ok_email_template_id = fields.Many2one(
    'mail.template',
    compute='_get_submission_ok_email_template_id',
    string=_("Successful email template"),
    store=False)
  crowdfunding_notification_request_ids = fields.One2many(
    'cm.crowdfunding.notification.request',
    'map_id',
    string=_("Notification requests"))


  # TODO: add constrains to not allow map creation without categories and presenters.
  @api.constrains('allow_filter_by_crowdfunding','crowdfunding_type','show_progress_on_marker')
  def _validate_crowdfunding_config(self):
    for record in self:
      if record.allow_filter_by_crowdfunding == True and record.crowdfunding_type == 'none':
        raise ValidationError(_("We can't have a crowdfunding filter if crowdfunding type is none"))
      if record.show_progress_on_marker == True and record.crowdfunding_type == 'none':
        raise ValidationError(_("We can't show progress on marker if crowdfunding type is none"))

  def get_config_datamodel_dict(self):
    return {
        "theme": self._get_theme_datamodel_dict(),
        "crowdfunding": self._get_crowdfunding_datamodel_dict(),
        "showFilters": self._get_filters_datamodel_dict(),
        "legal": self._get_legal_datamodel_dict(),
        "forms": self._get_form_models_datamodel_dict(),
        "suggestPlaceForms": self._get_proposal_form_models_datamodel_dict(),
        "categories": self._get_categories_datamodel_dict(),
        "categoriesInProposal": self._get_categories_inproposal_datamodel_dict()
    }
  def get_places_datamodel_dict(self):
    places = []
    for place in self.place_ids:
      if place.status == 'published' and place.team_type == 'map_place':
        places.append(place.get_datamodel_dict())
    return places

  def _get_theme_datamodel_dict(self):
    return {
      'color': self.colorschema_id.get_datamodel_dict(),
      'tileStyle': self.tile_style
    }
  def _get_crowdfunding_datamodel_dict(self):
    return {
      'showMarkerProgress': self.show_progress_on_marker,
    }

  @api.depends('proposal_form_model_id')
  def _get_submission_ok_message(self):
    for record in self:
      try:
        ok_message = record.proposal_form_model_id.submission_ok_message
      except:
        ok_message = False
      record.submission_ok_message = ok_message

  def _get_legal_datamodel_dict(self):
    legal = {
      'privacyLink': None,
      'cookiesLink': None
    }
    if self.privacy_link:
      legal['privacyLink'] = self.privacy_link
    if self.privacy_link:
      legal['cookiesLink'] = self.cookies_link
    return legal
  def _get_filters_datamodel_dict(self):
    return {
      'status': self.allow_filter_by_status,
      'crowdfunding': self.allow_filter_by_crowdfunding,
      'categories': self.allow_filter_by_category,
    }
  def _get_form_models_datamodel_dict(self):
    form_models = {}
    for form_model in self.allowed_form_model_mids:
      form_models[form_model.slug_id] = form_model.get_datamodel_dict()
    return form_models

  def _get_proposal_form_models_datamodel_dict(self):
    form_models = {}
    if self.proposal_form_model_id:
      form_models['suggest_place_generic'] = self.proposal_form_model_id.get_datamodel_dict(submission_form=False)
    for place_category in self.allowed_place_category_mids:
      if place_category.proposal_form_model_id:
        form_models[place_category.slug_id] = place_category.proposal_form_model_id.get_datamodel_dict(submission_form=False)
    if not form_models:
      return False
    return form_models

  def _get_categories_datamodel_dict(self):
    categories = {}
    for place_category in self.allowed_place_category_mids:
      categories[place_category.slug_id] = place_category.get_datamodel_dict()
    return categories

  def _get_categories_inproposal_datamodel_dict(self):
    categories = {}
    for place_category in self.allowed_place_category_inproposal_mids:
      categories[place_category.slug_id] = place_category.get_datamodel_dict()
    return categories

  # Form Submission
  def submit_place_proposal(self,data,category):
    # place creation
    place_creation_data = {
      'name': self.name + " (Place proposal)",
      'team_type': 'map_place_proposal',
      'map_id': self.id,
      'place_category_id': category.id,
      'user_id': self.env.user.id
    }
    if 'address' in data.keys():
      if 'latitude' in data['address'].keys():
        place_creation_data['lat'] = data['address']['latitude']
      if 'longitude' in data['address'].keys():
        place_creation_data['lng'] = data['address']['longitude']
      if 'address' in data['address'].keys():
        place_creation_data['address_txt'] = data['address']['address']
    place = self.env['crm.team'].create(place_creation_data)
    place.message_subscribe([self.env.user.partner_id.id])
    #  submission creation
    submission = self.env['crm.lead'].create({
      'name': self.name + " (Place Proposal Submission)",
      'submission_type': 'place_proposal_submission',
      'team_id': place.id
    })
    submission.write({
      'name': submission.name + " #" + str(submission.id)
    })
    # metadata & fields mapping
    # submission
    if category.proposal_form_model_id:
      proposal_form = category.proposal_form_model_id
      fields_map = proposal_form.json_place_proposal_submission_fields_map
      proposal_fields_map = category.proposal_form_model_id.json_place_proposal_fields_map
    else:
      proposal_form = self.proposal_form_model_id
      fields_map = proposal_form.json_place_proposal_submission_fields_map
      proposal_fields_map = self.proposal_form_model_id.json_place_proposal_fields_map
    submission.create_submission_metadata(data=data,fields_map=str(fields_map))
    # place
    proposal_update_dict = {
      'name': place.name + " #" +str(place.id),
      'proposal_form_submission_id': submission.id
    }
    if proposal_fields_map:
      jproposal_fields_map = json.loads(proposal_fields_map)
      for key in data.keys():
        if key in jproposal_fields_map.keys():
          if jproposal_fields_map[key]['model_field'] == 'number':
            value = float(data[key])
          else:#string
            value = str(data[key])
          proposal_update_dict[jproposal_fields_map[key]['model_field']] = value
          metadata = self.env['cm.form.submission.metadata'].search([
            ('submission_id','=',submission.id),
            ('key','=',key)
          ])
          if metadata.exists():
            metadata.write({'mapped_to': "proposal."+jproposal_fields_map[key]['model_field']})
    place.write(proposal_update_dict)
    place._get_slug_id()
    # Notifications
    if proposal_form.follower_partner_id:
      place.message_subscribe([proposal_form.follower_partner_id.id])
    place.message_post(
      subject=place.name+" notification",
      body="A new proposal has been made!",
      message_type="comment",
      subtype="mail.mt_comment"
    )
    return {
      'submission': submission,
      'place': place,
      'proposal_form': proposal_form
    }

  @api.depends('proposal_form_model_id')
  def _get_submission_ok_message(self):
    for record in self:
      try:
        ok_message = record.proposal_form_model_id.submission_ok_message
      except:
        ok_message = False
      record.submission_ok_message = ok_message

  @api.depends('proposal_form_model_id')
  def _get_submission_ok_email_template_id(self):
    for record in self:
      try:
        mail_template = record.proposal_form_model_id.submission_ok_email_template_id
      except:
        mail_template = False 
      record.submission_ok_email_template_id = mail_template.id

