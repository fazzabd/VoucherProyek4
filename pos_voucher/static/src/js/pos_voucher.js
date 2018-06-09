odoo.define('pos_voucher',function(require){
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');


//Custom Code
var VoucherButton = screens.ActionButtonWidget.extend({
    template: 'VoucherButton',

    button_click: function(){

    var self = this;
    self.custom_function();
    this.gui.show_popup('number', {
            'title':  _t('Voucher'),
            
        });

    },

    custom_function: function(){
        console.log('Hi I am button click of CustomButton');
    }

});

screens.define_action_button({
    'name': 'voucher_button',
    'widget': VoucherButton,
});

});
