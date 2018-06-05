# -*- coding : utf-8 -*- 
from odoo import models, fields, api
from datetime import datetime

class VoucherHistoryPOS(models.Model) :
	_name = 'history'
	_description = 'Voucher History'
	voucher_id = fields.Many2one('voucher','Voucher')
	name = fields.Char('Voucher Name', related='voucher_id.name')
	channel_used = fields.Selection([
		('posEco', 'Both POS & Ecommerce'),
		('eco', 'Ecommerce'),
		('pos', 'Point of Sales'),
		], string='Channel')
	user_id = fields.Many2one('res.partner','User',related='voucher_id.customer_id')
	create_date = fields.Datetime('Date',related='voucher_id.issue_date')
	voucher_value = fields.Float('Voucher Value',related='voucher_id.voucher_value')
	transaction_type = fields.Selection([
		('debit', 'Debit'),
		('credit', 'Credit'),
		], string='Transaction Type')
	order_id = fields.Many2one('sale.order','Sale Order')
	sale_order_line_id = fields.Many2one('sale.order.line','Sale order line id')
	state = fields.Selection([
		('draft','Draft'),
		],string='State')
	pos_order_id = fields.Many2one('pos.order','Pos Order Id')
	pos_order_line_id = fields.Many2one('pos.order.line','Pos Line Id')
	description = fields.Text('Description',related='voucher_id.note')