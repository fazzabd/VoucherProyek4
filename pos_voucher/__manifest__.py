{
    'name': 'Voucher and Coupon',
    'summary': "Odoo POS Vouchers",
    'description': """Now enhance your sale using our module “Odoo POS Vouchers”. This module allows you to create and redeem vouchers/coupons from Point of Sale.
	Using “Odoo POS Vouchers”, you can provide special offers to the customers and also it plays an important role in reactivating your old customers because they are already aware of your services and would be attracted if you provide them special discounts/offers.
	A POS user creates vouchers for the customers in which specific code is mentioned. This code is used to provide a flat or percent based discount, on customers order.
    """,
    'author': 'A2 JTK 2016 Semester 4',
    'depends': ['point_of_sale','sale','base','mail'],
    'data': [
		'views/pos_voucher_views.xml',
		'views/voucher_view.xml',
		'views/voucherconfig_view.xml',
        'report/voucher_report.xml',
        'report/voucher_template.xml',
        #'views/history_view.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/ir_sequence_data.xml',
		],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
