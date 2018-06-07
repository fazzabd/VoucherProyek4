odoo.define('pos_voucher',function(require){
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var _t  = require('web.core')._t;
// var PosBaseWidget = require('point_of_sale.BaseWidget');
// var pos_popup = require('point_of_sale.popups');
//Custom Code
var VoucherButton = screens.ActionButtonWidget.extend({
    template: 'VoucherButton',

    button_click: function(){

    var self = this;
    this.gui.show_popup('textinput', {
            'title':  _t('Redeem Gift Coupon'),
            // 'confirm': function(value) {
            //          this.gui.close_popup();
            //     },
        });

    },

});

screens.define_action_button({
    'name': 'voucher_button',
    'widget': VoucherButton,
});

});
