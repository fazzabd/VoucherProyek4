# -*- coding : utf-8 -*- 
from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta

import random
import string

class VoucherPOS(models.Model) :
	_name = 'voucher'
	_inherit=['mail.thread']
	_description = 'Voucher POS'
	
	name = fields.Char('Name',required=True)
	voucher_code = fields.Char('Code')
	voucher_usage = fields.Selection([
        ('posEcommerce', 'Both POS & Ecommerce'),
		('eco', 'Ecommerce'),
        ('pos', 'Point of Sales'),
        ], string='Coupon Used In',default='posEcommerce', required=True)
	customer_type = fields.Selection([
        ('specific', 'Specific Customer'),
        ('all', 'All Customer'),
        ], string='Coupon For', default='specific', required=True)
	customer_id = fields.Many2one('res.partner','Created For', required=True)
	active = fields.Boolean('Active',default=True)
	validity = fields.Integer('Validity(In days)')
	expiry_date = fields.Date('Expiry Date')
	issue_date = fields.Date('Applicable From',default=datetime.now(),required=True)
	voucher_val_type = fields.Selection([
        ('persen', '%'),
        ('fix', 'Fixed'),
        ], string='Voucher val type')
	voucher_value = fields.Float('Voucher Value',required=True)
	minimum_cart_amount = fields.Float('Minimum Cart Amount',required=True)
	use_minimum_cart_value = fields.Boolean('Use Cart Amount Validation')
	is_partially_redemed = fields.Boolean('Use Partial Redemption')
	redeemption_limit = fields.Integer('Max Redemption Limit',required=True)
	applied_on = fields.Selection([
		('all', 'All Products'),
        ('specific', 'Specific Product'),
        ], string='Voucher Applied On',required=True)
	product_ids = fields.Many2many('product.template')
	display_desc_in_web = fields.Boolean('Display Description in Website',default=True)
	note = fields.Text('Description')
	

	# @api.model
	# def _get_default_code():
 #    	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))