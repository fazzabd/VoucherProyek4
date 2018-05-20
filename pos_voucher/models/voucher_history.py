# -*- coding : utf-8 -*-
from odoo import models, fields
from datetime import datetime
from datetime import timedelta

class VoucherHistory(models.Model) :
	_name = 'history'
	_description = 'Voucher History'

    name = fields.Char('Voucher Name',required=True)
    # channel_used = fields.Selection([
    #     ('posEco', 'Both POS & Ecommerce'),
	# 	('eco', 'Ecommerce'),
    #     ('pos', 'Point of Sales'),
    #     ], string='Channel')
    # user_id = fields.Many2one('res.partner','User')
    # create_date = fields.Datetime('Date')
    # voucher_value = fields.Float('Voucher Value')
    # transaction_type = fields.Selection([
    #     ('debit', 'Debit'),
	# 	('credit', 'Credit'),
    #     ], string='Transaction Type')
    # order_id = fields.Many2one('sale.order','Sale Order')
    # sale_order_line_id = fields.Many2one('sale.order.line','Sale order line id')
    # voucher_id = fields.Many2one('voucher','Voucher')
	# state = fields.Selection([
	# 	('draft','Draft'),
	# 	],string='State')
	# pos_order_id = fields.Many2one('pos.order','Pos Order Id')
	# pos_order_line_id = fields.Many2one('pos.order.line','Pos Line Id')
	# Description = fields.Text('Description')
