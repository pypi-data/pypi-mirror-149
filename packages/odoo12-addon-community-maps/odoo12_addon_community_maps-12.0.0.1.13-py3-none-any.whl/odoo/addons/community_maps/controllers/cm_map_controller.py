from werkzeug.exceptions import BadRequest, NotFound
from odoo.addons.base_rest.controllers import main
from odoo.http import route

class CmMapController(main.RestController):
  _root_path = "/api/private/"
  _collection_name = "base_rest.private_services"
  _default_auth = "api_key"

  @route([
    _root_path + 'maps/<string:_map_slug>/places',
    _root_path + 'maps/<string:_map_slug>/places/<string:_place_slug>'
  ], methods=['GET'], auth="api_key", csrf=False)
  def places(self, _map_slug, _place_slug=None, **params):
    return self._process_method('maps', 'places', _map_slug, _place_slug)

  @route([
    _root_path + 'maps/forms',
  ], methods=['POST'], auth="api_key", csrf=False)
  def forms(self, **params):
    return self._process_method('maps', 'forms',params)