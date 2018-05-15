# -*- coding : utf-8 -*-
from odoo import models, fields
from datetime import datetime
from datetime import timedelta

class VoucherConfigPos(models.Model) :
	_name = 'voucher.config'
	_description = 'Voucher Configuration'

	active =  fields.Boolean('Active')
	customer_type = fields.Selection([
        ('specific', 'Specific Customer'),
        ('all', 'All Customer'),
        ], string='Customer Type', required=True)
	default_availability = fields.Integer('Total Available',required=True)
	default_name = fields.Char('Name',required=True)
	default_validity = fields.Integer('Validity(in days)', required=True)
	default_value = fields.Float('Voucher Value', required=True)
	max_amount = fields.Float('Maximum Voucher Value', required=True)
	max_expiry_date = fields.Date('Maximum Expiry Date', required=True)
	min_amount = fields.Float('Minimum Voucher Value', required=True)
	minimum_cart_amount = fields.Float('Minimum Cart Amount')
	name = fields.Char('Name')
	partial_limit = fields.Integer('Partial Limit')
	partially_use = fields.Boolean('Partially Use')
	product_id = fields.Many2one('product.product', 'Product', required=True)
	use_minimum_cart_value = fields.Boolean('Use Cart Amount Validation')
	