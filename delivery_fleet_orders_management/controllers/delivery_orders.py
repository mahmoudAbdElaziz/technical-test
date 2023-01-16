import functools
import logging
import datetime

try:
    import simplejson as json
except ImportError:
    import json
from odoo import http, _
from odoo.http import request
from odoo import fields

_logger = logging.getLogger(__name__)


def valid_request_data(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        request_data = json.loads(request.httprequest.data)

        try:
            from_date = datetime.datetime.strptime(request_data['from_date'], '%Y-%m-%d')
            to_date = datetime.datetime.strptime(request_data['to_date'], '%Y-%m-%d')
        except ValueError:
            info = "Incorrect data format, should be YYYY-MM-DD"
            return {
                'error': "ValidationError",
                'errorDescription': info,
            }

        if from_date > to_date:
            info = "to_date must be greeter than or equal from_date"
            return {
                'error': "ValidationError",
                'errorDescription': info,
            }

        return func(self, *args, **kwargs)

    return wrap


class ControllerREST(http.Controller):
    """
        How To Use API:
        GET /api/driver/1/orders HTTP/1.1
        Host: your_server_url
        Content-Type: application/json
        {
            "from_date": "2022-09-28",
            "to_date":"2022-09-30"
        }
    """

    @http.route('/api/driver/<int:driver_id>/orders', methods=['GET'], type='json', auth='none', csrf=False)
    @valid_request_data
    def get_driver_orders(self, driver_id):
        request_data = json.loads(request.httprequest.data)
        from_date = fields.Date.from_string(request_data['from_date'])
        to_date = fields.Date.from_string(request_data['to_date'])
        vals = []
        orders = request.env['stock.picking'].sudo().search(
            [('driver_id', '=', int(driver_id)), ('scheduled_date', '>=', from_date),
             ('scheduled_date', '<=', to_date)])
        for order in orders:
            vals.append({
                'name': order.name,
                'scheduled_date': order.scheduled_date,
                'from': order.location_id.name,
                'to': order.location_dest_id.name,
                'state': order.state,
            })

        return {"data": vals}
