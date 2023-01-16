{
    'name': 'Delivery Fleet Orders Management',
    'version': '1.0.0',
    'category': 'Fleet',
    'depends': ['stock', 'fleet', 'stock_enterprise', 'report_xlsx'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
        'views/fleet_vehicle_views.xml',
        'wizards/delivery_fleet_orders_wizard.xml',
        'report/fleet_orders_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
