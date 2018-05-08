# -*- coding : utf-8 -*-
from odoo import models, fields


class VoucherConfigPos(models.Model) :
	_name = 'voucher.config'
	_description = 'Voucher Configuration'
	
	__last_update = fields.datetime( required=True)
	active =  fields.boolean('Active',  required=True)
	create_date = fields.datetime( required=True)
	create_uid = fields.many2one( required=True)
	customer_type = fields.selection('Customer Type')
	default_availability = fields.integer('Total Available',  required=True)
	default_name = fields.char( required=True)
	default_validity = fields.integer('Validity(in days)',  required=True)
	default_value = fields.float('Voucher Value',  required=True)
	display_name = fields.char( required=True)
	id = fields.integer( required=True)
	max_amount = fields.float('Maximum Voucher Value',  required=True)
	max_expiry_date = fields.date('Maximum Expiry Date',  required=True)
	min_amount = fields.float('Minimum Voucher Value',  required=True)
	minimum_cart_amount = fields.float('Minimum Cart Amount',  required=True)
	name = fields.char('Name',  required=True)
	partial_limit = fields.integer('Partial Limit',  required=True)
	partially_use = fields.boolean('Partially Use',  required=True)
	product_id = fields.many2one('Product',  required=True)
	use_minimum_cart_value = fields.boolean('Use Cart Amount Validation',  required=True)
	voucher_usage = fields.selection('Coupon Used In',  required=True)
	write_date = fields.datetime( required=True)
	write_uid = fields.many2one( required=True)
	