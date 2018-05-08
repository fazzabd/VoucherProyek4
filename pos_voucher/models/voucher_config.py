# -*- coding : utf-8 -*-
from odoo import models, fields
from datetime import datetime
from datetime import timedelta

class VoucherConfigPos(models.Model) :
	_name = 'voucher.config'
	_description = 'Voucher Configuration'

	active =  fields.Boolean('Active', required=True)
	create_date = fields.Datetime('Created On',required=True)
	create_uid = fields.Many2one('res.users', 'Created by',required=True)
	customer_type = fields.Selection([
        ('specific', 'Specific Customer'),
        ('all', 'All Customer'),
        ], string='Customer Type', required=True)
	default_availability = fields.Integer('Total Available',required=True)
	default_name = fields.Char('Name',required=True)
	default_validity = fields.Integer('Validity(in days)', required=True)
	default_value = fields.Float('Voucher Value', required=True)
	display_name = fields.Char('Display Name',required=True)
	id = fields.Integer('ID',required=True)
	max_amount = fields.Float('Maximum Voucher Value', required=True)
	max_expiry_date = fields.Date('Maximum Expiry Date', required=True)
	min_amount = fields.Float('Minimum Voucher Value', required=True)
	minimum_cart_amount = fields.Float('Minimum Cart Amount', required=True)
	name = fields.Char('Name')
	partial_limit = fields.Integer('Partial Limit', required=True)
	partially_use = fields.Boolean('Partially Use', required=True)
	product_id = fields.Many2one('product.product', 'Product', required=True)
	use_minimum_cart_value = fields.Boolean('Use Cart Amount Validation', required=True)
	voucher_usage = fields.Selection([
        ('posEcommerce', 'Both POS & Ecommerce'),
		('eco', 'Ecommerce'),
        ('pos', 'Point of Sales'),
        ], string='Coupon Used In', required=True)
	write_date = fields.Datetime('Last Updated On', required=True)
	write_uid = fields.Many2one('res.users','Last Updated By', required=True)
	