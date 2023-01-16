from odoo import _, api, fields, models


class DeliveryFleetOrdersWizard(models.TransientModel):
    _name = "delivery.fleet.orders.wizard"
    _description = "Delivery Fleet Orders Wizard"

    vehicle_ids = fields.Many2many('fleet.vehicle', string="Vehicles", required=True)
    driver_ids = fields.Many2many('res.partner', string="Drivers")
    date_from = fields.Date(default=lambda self: fields.Date.today(), required=True)
    date_to = fields.Date(default=lambda self: fields.Date.today(), required=True)

    def get_order_ids(self):
        domain = [('vehicle_id', 'in', self.vehicle_ids.ids), ('scheduled_date', '>=', self.date_from),
                  ('scheduled_date', '<=', self.date_to)]
        if self.driver_ids:
            domain.append(('driver_id', 'in', self.driver_ids.ids))
        orders = self.env['stock.picking'].search(domain)
        return orders

    def print_pdf_report(self):
        orders = self.get_order_ids()
        return self.env.ref('delivery_fleet_orders_management.fleet_orders_report').report_action(orders)

    def print_xlsx_report(self):
        orders = self.get_order_ids()
        return self.env.ref('delivery_fleet_orders_management.fleet_orders_xlsx').report_action(orders)

    def redirect_to_stock_report_dashboard(self):
        action = self.env.ref('stock_enterprise.stock_report_dashboard_action').sudo().read()[0]
        orders = self.get_order_ids()
        if orders:
            domain = [('picking_id', '=', orders.ids)]
        else:
            domain = [('picking_id', '=', False)]

        action['domain'] = domain
        return action
