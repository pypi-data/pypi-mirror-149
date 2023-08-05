import json
from odoo.addons.base_rest import restapi
from werkzeug.exceptions import BadRequest, NotFound
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component
from odoo.addons.base_rest_base_structure.models.api_services_utils import APIServicesUtils
from odoo.tools.translate import _
from odoo.http import Response


class CmMapService(Component):
  _inherit = "base.rest.private_abstract_service"
  _name = "cm.map.service"
  _usage = "maps"
  _description = """
      Map Service
  """

  @restapi.method(
    [(["/<string:slug>/config"], "GET")],
    auth="api_key",
  )
  def config(self,_slug):
    record = self.env["cm.map"].search(
      [("slug_id", "=", _slug)]
    )
    if record:
      try:
        record.ensure_one()
      except:
        return Response(
          json.dumps({'message':_("More than one map found for %s") % _slug}),
          status=404,
          content_type="application/json")
      return record.get_config_datamodel_dict()
    else:
      return Response(
        json.dumps({'message':_("No map record for id %s") % _slug}),
        status=404,
        content_type="application/json")
    return False

  def forms(self,params={}):
    if params:
      if 'type' in params.keys() and 'slug' in params.keys() and 'data' in params.keys():
        # PLACE SUBMISSION
        if params['type'] == 'place':
          ok_response = self._forms_submission(params['slug'],params)
          if ok_response:
            return ok_response
          
        # PROPOSAL SUBMISSION
        if params['type'] == 'suggestPlace':
          return_data = self._forms_proposal(params)
        if return_data:
          # Create submission at same time of creating proposal
          if return_data['proposal_form'].generate_submission_in_proposal:
            # overwrite slug param with place slug in order to create correct submission
            params['slug'] = return_data['place'].slug_id
            self._forms_submission(
              return_data['place'].slug_id,
              params,
              return_data['proposal_form'].json_submission_fields_map
            )
          return return_data['ok_response']

    return Response(
      json.dumps({'message':_("Bad request.")}),
      status=400,
      content_type="application/json")

  def _forms_submission(self,place_slug,params,submission_fields_map=False):
    place_records = self.env["crm.team"].search([
      ("slug_id", "=", place_slug),
      ("team_type", "in", ['map_place','map_place_proposal'])
    ])
    if place_records.exists():
      place_record = place_records[0]
      # submit
      if 'mapUrl' in params.keys():
        params['data']['shareable_url'] = params['mapUrl']+"?mapPlace="+ params['slug']

      place_submission = place_record.submit_place_form(params['data'],submission_fields_map)
      # email
      if place_record.submission_ok_email_template_id:
        place_record.submission_ok_email_template_id.send_mail(place_submission.id,force_send=True)
      # client mesage
      return {'message': place_record.submission_ok_message}
    return False

  def _forms_proposal(self,params):
    if 'mapSlug' in params.keys():
      map_record = self.env["cm.map"].search([
        ("slug_id", "=", params['mapSlug'])
      ])
      category_record = self.env["cm.place.category"].search([
        ("slug_id", "=", params['slug'])
      ])
      if map_record.exists() and category_record.exists():
        # submit
        return_data = map_record.submit_place_proposal(params['data'],category_record)
        proposal_submission = return_data['submission']
        # email
        if category_record.submission_ok_email_template_id:
          submission_ok_email_template = category_record.submission_ok_email_template_id
        else:
          submission_ok_email_template = map_record.submission_ok_email_template_id
        if submission_ok_email_template:
          submission_ok_email_template.send_mail(proposal_submission.id,force_send=True)
        # client message
        if category_record.submission_ok_message:
          ok_msg = category_record.submission_ok_message
        else:
          ok_msg = map_record.submission_ok_message
        return {
          'ok_response':{'message': ok_msg},
          'place': return_data['place'],
          'proposal_form': return_data['proposal_form']
        }
    return False

  def places(self,_map_slug,_place_slug=None):
    record = self.env["cm.map"].search([
      ("slug_id", "=", _map_slug)
    ])
    if record.exists():
      try:
        record.ensure_one()
      except:
        return Response(
          json.dumps({'message':_("More than one map found for %s") % _map_slug}),
          status=404,
          content_type="application/json")
      if _place_slug:
        place_record = self.env["crm.team"].search([
          ("slug_id", "=", _place_slug),
          ("team_type", "=", 'map_place'),
          ("status", "=", 'published')
        ])
        if place_record.exists():
          try:
            place_record.ensure_one()
          except:
            return Response(
              json.dumps({'message':_("More than one place found for %s") % _place_slug}),
              status=404,
              content_type="application/json")
          return place_record.get_datamodel_dict(True)
        else:
          return Response(
            json.dumps({'message':_("No place record for id %s") % _place_slug}),
            status=404,
            content_type="application/json")
      else:
        return record.get_places_datamodel_dict()
    else:
      return Response(
            json.dumps({'message':_("No map record for id %s") % _map_slug}),
            status=404,
            content_type="application/json")
    return False
