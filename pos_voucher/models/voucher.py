# -*- coding : utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta
import logging

class VoucherPOS(models.Model) :
    _name = 'voucher'
    _inherit=['mail.thread']
    _description = 'Voucher POS'

    @api.model
    def _current_value(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.default_value
    
    @api.model
    def _current_cust(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.customer_type
    
    @api.model
    def _current_usage(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.voucher_usage
        
    @api.model
    def _current_validity(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.default_validity
    
    @api.model
    def _current_mca(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.minimum_cart_amount
    
    @api.model
    def _current_umcv(self):
        value = self.env['voucher.config'].search([('id','=',1)])[0]
        return value.use_minimum_cart_value
        
    name = fields.Char('Name',required=True)
    voucher_code = fields.Char('Code', index=True)
    voucher_usage = fields.Selection([
    ('posEcommerce', 'Both POS & Ecommerce'),
    ('eco', 'Ecommerce'),
    ('pos', 'Point of Sales'),
    ], string='Coupon Used In',default=_current_usage, required=True)
    customer_type = fields.Selection([
    ('specific', 'Specific Customer'),
    ('all', 'All Customer'),
    ], string='Coupon For', default=_current_cust, required=True)
    customer_id = fields.Many2one('res.partner','Created For')
    active = fields.Boolean('Active',default=True)
    validity = fields.Integer('Validity(In days)',default=_current_validity)
    expiry_date = fields.Datetime('Expiry Date')
    issue_date = fields.Datetime('Applicable From',default=datetime.now(),required=True)
    voucher_val_type = fields.Selection([
    ('persen', '%'),
    ('fix', 'Fixed'),
    ], string='Voucher val type', default='persen', required=True)
    voucher_value = fields.Float('Voucher Value',default=_current_value, required=True)
    minimum_cart_amount = fields.Float('Minimum Cart Amount',default=_current_mca)
    use_minimum_cart_value = fields.Boolean('Use Cart Amount Validation',default=_current_umcv)
    is_partially_redemed = fields.Boolean('Use Partial Redemption')
    redeemption_limit = fields.Integer('Max Redemption Limit')
    applied_on = fields.Selection([
    ('all', 'All Products'),
    ('specific', 'Specific Product'),
    ], string='Voucher Applied On',default='all', required=True)
    product_ids = fields.Many2many('product.template')
    display_desc_in_web = fields.Boolean('Display Description in Website',default=True)
    note = fields.Text('Description')

    @api.multi
    def send_mail_to_customers(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'voucher',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # @api.model
    # def create(self, vals):
    #     seq = self.env['ir.sequence'].get('voucher') or '/'
    #     vals['voucher_code'] = seq
    #     return super(VoucherPOS, self).create(vals)

    @api.model
    def create(self, vals):
        if vals['voucher_code']:
            record = super(VoucherPOS, self).create(vals)
        else:
            seq = self.env['ir.sequence'].get('voucher') or '/'
            vals['voucher_code'] = seq
            record = super(VoucherPOS, self).create(vals)
        # search_ids = self.pool.get('voucher').search(cr, uid, [])
        # last_id = search_ids and max(search_ids)
        self.env['history'].create({
            'name': record.name,
            'voucher_value': record.voucher_value,
            'channel_used': record.voucher_usage,
            #'user_id': record.customer_id,
            'create_date': record.issue_date,
            'voucher_id' : record.id,
            # 'transaction_type': record.
            # 'order_id': record.
            # 'sale_order_line_id': record.
            # 'pos_order_id': record.
            # 'pos_order_line_id': record.
            'transaction_type': 'credit',
            'state': 'draft',
            'description': record.note,
        })
        return record
