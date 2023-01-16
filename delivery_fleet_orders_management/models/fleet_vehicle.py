# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    picking_ids = fields.One2many('stock.picking', 'vehicle_id',
                                  # domain=[('picking_type_code', '=', 'outgoing'),
                                  #         ('scheduled_date', '>=', fields.Datetime.today())],
                                  string="Delivery Orders")
    all_orders_count = fields.Integer(compute="_compute_orders_count", store=True)
    future_orders_count = fields.Integer(compute="_compute_orders_count", store=True)
    today_orders_count = fields.Integer(compute="_compute_orders_count", store=True)

    @api.depends('picking_ids')
    def _compute_orders_count(self):
        for rec in self:
            rec.all_orders_count = len(rec.picking_ids)
            rec.today_orders_count = len(
                rec.picking_ids.filtered(
                    lambda line: line.scheduled_date.strftime('%Y-%m-%d') == fields.Date.today().strftime('%Y-%m-%d')))
            rec.future_orders_count = len(
                rec.picking_ids.filtered(lambda line: line.scheduled_date >= fields.Datetime.today()))

    def action_redirect_to_picking_orders(self):
        action = self.env.ref('stock.stock_picking_action_picking_type').sudo().read()[0]
        action['context'] = {'active_test': False, 'create': False, 'delete': False}
        all_orders = self._context.get('all_orders', False)
        domain = [('vehicle_id', '=', self.id)]
        if not all_orders:
            domain.append(('scheduled_date', '>=', fields.Datetime.today()))
        action['domain'] = domain
        return action

    def action_send_notification(self):
        for vehicle in self:
            if vehicle.picking_ids.filtered(lambda line: line.state in (
                    'assigned', 'waiting', 'confirmed') and line.scheduled_date >= fields.Datetime.today()):
                body = _(
                    'You Have Pending Orders, Please Check Vehicle '
                    '<a href=# data-oe-model=fleet.vehicle data-oe-id=%d>%s</a>') % (vehicle.id, vehicle.name)
                vehicle.message_post(body=body, partner_ids=[vehicle.driver_id.id])
