# -*- coding : utf-8 -*- 
from odoo import models, fields
from datetime import datetime
from datetime import timedelta

class VoucherPOS(models.Model) :
	_name = 'voucher'
	_description = 'Voucher POS'
	
	name = fields.Char('Name',required=True)
	voucher_code = fields.Char('Code')
	voucher_usage = fields.Selection([
        ('posEcommerce', 'Both POS & Ecommerce'),
        ('pos', 'Point of Sales'),
        ], string='Coupon Used In', required=True)
	customer_type = fields.Selection([
        ('specific', 'Specific Customer'),
        ('all', 'All Customer'),
        ], string='Coupon For', required=True)
	customer_id = fields.Many2one('res.partner','Created For',required=True)
	active = fields.Boolean('Active')
	validity = fields.Integer('Validity(In days)')
	expiry_date = fields.Date('Expiry Date')
	issue_date = fields.Date('Applicable From',required=True)
	voucher_val_type = fields.Selection([
        ('persen', '%'),
        ('fix', 'Fixed'),
        ], string='Voucher val type')
	voucher_value = fields.Float('Voucher Value')
	minimum_cart_amount = fields.Float('Minimum Cart Amount')
	use_minimum_cart_value = fields.Boolean('Use Cart Amount Validation')
	is_partially_redemed = fields.Boolean('Use Partial Redemption')
	redeemption_limit = fields.Integer('Max Redemption Limit')
	applied_on = fields.Selection([
		('all', 'All Products'),
        ('specific', 'Specific Product'),
        ], string='Voucher Applied On')
	product_ids = fields.Many2many('product.template','Products')
	display_desc_in_web = fields.Boolean('Display Description in Website')
	note = fields.Text('Description')
