# -*- coding : utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta

class VoucherPOS(models.Model) :
    _name = 'voucher'
    _inherit=['mail.thread']
    _description = 'Voucher POS'
    # _inherits = {'history': 'hist_id'}

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
    customer_id = fields.Many2one('res.partner','Created For')
    active = fields.Boolean('Active',default=True)
    validity = fields.Integer('Validity(In days)')
    expiry_date = fields.Datetime('Expiry Date')
    issue_date = fields.Datetime('Applicable From',default=datetime.now(),required=True)
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
    ], string='Voucher Applied On',default='specific', required=True)
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

    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        # Do your custom logic here
        record = self.env['history'].create({'voucher_id': self.id})
        return super(VoucherPOS, self).create(values)

  #   @api.multi
  #   def write(self, values):
  #       """Override default Odoo write function and extend."""
  #       # Do your custom logic here
  #       record_ids = self.env['history'].search([('voucher_id', '=', self.id)])
		# for record in record_ids:
  #   		record.write({'some_field': 'some_description'})
  #       return super(ResPartner, self).write(values)