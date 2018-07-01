odoo.define('pos_voucher',function(require){
"use strict";

var core = require('web.core');
var pos_screen = require('point_of_sale.screens');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var pos_model = require('point_of_sale.models');
var pos_popup = require('point_of_sale.popups');
var gui = require('point_of_sale.gui');
var models = pos_model.PosModel.prototype.models;
var PosModelSuper = pos_model.PosModel;
var OrderSuper = pos_model.Order;
var Model = require('web.DataModel');
var core = require('web.core');
var _t = core._t;
var utils = require('web.utils');
var round_pr = utils.round_precision;
// var PosBaseWidget = require('point_of_sale.BaseWidget');
// var pos_popup = require('point_of_sale.popups');
//Custom Code

    function find_voucher(code, vouchers) {
        var voucher = [];
        for(var i in vouchers){
            if (vouchers[i]['voucher_code'] == code){
                voucher.push(vouchers[i]);
                return voucher;
            }
        }
        return false;
    }

    function check_validity(voucher,vouchers, customer) {
        // checking it is already used or not
        for (var i in vouchers){
            if(vouchers[i]['voucher_code'] == voucher[0]['voucher_code'] && vouchers[i]['customer_id'][0] == customer['id']){
                return vouchers[i];
            }
        }
        return false;
    }

    function check_expiry(start, end) {
        var today = moment().format('YYYY-MM-DD HH:mm:ss');
        if(start && end) {
            if (today < start || today > end)
                return false;
        }
        else if(start){
            if (today < start)
                return false;
        }
        else if(end){
            if (today > end)
                return false;
        }
        return true;
    }

    function get_coupon_product(products) {
        for (var i in products){
            if(products[i]['display_name'] == 'Gift-Coupon')
                return products[i]['id'];
        }
        return false;
    }

    // getting vouchers and coupons
    models.push(
        {
            model: 'voucher',
            fields: ['id', 'voucher_code', 'name','customer_id','validity', 'active', 'expiry_date','issue_date',
             'voucher_val_type','voucher_value','redeemption_limit','product_ids'],
            loaded: function (self, vouchers) {
                    self.vouchers = vouchers;
            },  
        },
        {
            model: 'history',
            fields: ['id', 'name','voucher_value','channel_used','user_id','create_date', 'voucher_id', 
            'transaction_type', 'state' , 'description'],
            loaded: function (self, histo) {
                    self.histo = histo;
            },
        }
        );

var VoucherWidget = PosBaseWidget.extend({
        template:'VoucherWidget',        
        init: function(parent) {
            return this._super(parent);
        },
        renderElement: function () {
            var self = this;
            this._super();
            this.$(".coupons").click(function () {
                self.gui.show_popup('coupon',{
                    'title': _t('Enter your Coupon'),
                });
            });
        },
    });

// PosModel is extended to store vouchers, & coupon details
    pos_model.PosModel = pos_model.PosModel.extend({
        initialize: function(session, attributes) {
            PosModelSuper.prototype.initialize.call(this, session, attributes)
            this.vouchers = [];
            this.histo = [];
        },
    });
    
    pos_model.Order = pos_model.Order.extend({
        initialize: function(attributes,options){
            this.coupon = false;
            this.coupon_status = [];
            return OrderSuper.prototype.initialize.call(this, attributes,options);;
        },
        set_coupon_value: function (coupon) {
            this.coupon_status = coupon;
            return;
        },
        coupon_applied: function () {
            this.coupon = true;
            this.export_as_JSON();
            return;
        },
        // check_voucher_validy: function () {
        //     var self = this;
        //     var order = self.pos.get_order();
        //     var vouchers = self.pos.vouchers;
        //     var voucher = null;
        //     for (var i in vouchers){
        //         if(vouchers[i]['id'] == self.coupon_status.voucher[0]){
        //             voucher = vouchers[i];
        //             break;
        //         }
        //     }
        //     var flag ;
        //     if(voucher){
        //         switch(voucher.voucher_type){
        //             case 'product': {
        //                 var lines = order.orderlines.models;
        //                 var products = {};
        //                 for (var p in lines){
        //                     products[lines[p].product.id] = null;
        //                 }
        //                 if(voucher.product_id[0] in products){
        //                     flag = true;
        //                 }
        //                 else
        //                     flag = false;
        //                 break;
        //             }
        //             case 'category':{
        //                 var lines = order.orderlines.models;
        //                 var category = {};
        //                 for (var p in lines){
        //                     if(lines[p].product.pos_categ_id){
        //                         category[lines[p].product.pos_categ_id[0]] = null;
        //                     }
        //                 }
        //                 if(voucher.product_categ[0] in category){
        //                     flag = true;
        //                 }
        //                 else
        //                     flag = false;
        //                 break;
        //             }
        //             case 'all': flag = true; break;
        //             default: break;
        //         }
        //     }
        //     return flag;
        // },
        export_as_JSON: function () {
            var self = OrderSuper.prototype.export_as_JSON.call(this);
            self.coupon = this.coupon;
            self.coupon_status = this.coupon_status;
            return self;
        },
        init_from_JSON: function(json) {
            this.coupon = json.coupon;
            this.coupon_status = json.coupon_status;
            OrderSuper.prototype.init_from_JSON.call(this, json);
        },
        get_total_without_tax: function() {
            var res = OrderSuper.prototype.get_total_without_tax.call(this);
            var final_res = round_pr(this.orderlines.reduce((function(sum, orderLine) {
                return sum + (orderLine.get_unit_price() * orderLine.get_quantity() * (1.0 - (orderLine.get_discount() / 100.0)));
            }), 0), this.pos.currency.rounding);
            return final_res;
        },
    });

pos_screen.ProductScreenWidget.include({
        start: function(){ 
            this._super();
            this.coupons = new VoucherWidget(this,{});
            this.coupons.replace(this.$('.placeholder-VoucherWidget'));
        },
    });

var CouponPopupWidget = pos_popup.extend({
        template: 'CouponPopupWidget',
        init: function(parent) {
            this.coupon_product = null;
            return this._super(parent);
        },
        show: function(options){
            options = options || {};
            this._super(options);
            if(!this.coupon_product)
                this.coupon_product = get_coupon_product(this.pos.db.product_by_id);
            this.flag = true;
            this.coupon_res = [];
            this.coupon_status = [];
            this.renderElement();
            this.$('input').focus();
        },
        click_confirm: function(){
            var value = this.$('input').val();
            this.gui.close_popup();
            if( this.options.confirm ){
                this.options.confirm.call(this,value);
            }
        }, 
        renderElement: function () {
            this._super();
            var self = this;

            this.$(".validate_coupon").click(function () {
                // checking the code entered
                var current_order = self.pos.get_order();
                var coupon = $(".coupon_code").val();
                if (current_order.orderlines.models.length == 0){
                    self.gui.show_popup('error',{
                        'title': _t('No products !'),
                        'body': _t('You cannot apply coupon without products.'),
                    });
                }
                else if(coupon){
                    //if(self.pos.get_client()){
                        var customer = self.pos.get_client();
                        var coupon_res = find_voucher(coupon, self.pos.vouchers);
                        var flag = true;
                        // is there a coupon with this code which has balance above zero
                        
                        //Teredit dari sini
                        if (coupon_res) {
                            // checking coupon status
                            var coupon_stat = true //check_validity(coupon_res, self.pos.vouchers , customer);
                            // if this coupon was for a particular customer and is not used already
                            if(coupon_res[0]['customer_id'] && coupon_res[0]['customer_id'][0] != customer['id']){
                                flag = false;
                            }
                            var today = moment().format('YYYY-MM-DD HH:mm:ss');
                            // checking coupon balance and expiry
                            if(flag && coupon_stat){
                                // checking coupon validity
                                flag = check_expiry(coupon_res[0]['issue_date'], coupon_res[0]['expiry_date']);
                            }
                            // this customer has not used this coupon yet
                            else if(flag && !coupon_stat){
                                flag = check_expiry(coupon_res[0]['issue_date'], coupon_res[0]['expiry_date']);
                            }
                            else{
                                flag = false;
                                $(".coupon_status_p").text("Unable to apply coupon. Check coupon validity.!");
                            }
                        }else{
                            flag = false;
                            $(".coupon_status_p").text("Invalid code. Please try again !!");
                        }
                        // flag = true;
                        if(flag){
                            var val = coupon_res[0]['voucher_val_type'] == 'fix' ?
                                coupon_res[0]['voucher_value'] : coupon_res[0]['voucher_value'] + "%";
                            var obj = $(".coupon_status_p").text("voucher value is : "+val+" \n" +
                                " Do you want to proceed ? \n This operation cannot be reversed.");
                            obj.html(obj.html().replace(/\n/g,'<br/>'));
                            var order = self.pos.get_order();
                            order.set_coupon_value(coupon_res[0]);
                        }
                        self.flag = flag;
                        if(flag){
                           $(".confirm-coupon").css("display", "block");
                           self.coupon_res = coupon_res;
                           //self.flag = true;
                        }
                        else{
                            var ob = $(".coupon_status_p").text("Invalid code or no coupons left. \nPlease check coupon validity.\n" +
                                "or check whether the coupon usage is limited to a particular customer.");
                            ob.html(ob.html().replace(/\n/g,'<br/>'));
                            //self.flag = false;
                        }
                    // }
                    // else{
                    //     $(".coupon_status_p").text("Please select a customer !!");
                    // }
                }

            });
            this.$(".confirm-coupon").click(function () {
                // verifying and applying coupon
                if(self.flag){
                    var order = self.pos.get_order();
                    var lines = order ? order.orderlines : false;
                    // if(order.coupon){
                    //     self.gui.close_popup();
                    //     self.gui.show_popup('error',{
                    //         'title': _t('Unable to apply coupon !'),
                    //         'body': _t('Either coupon is already applied or you have not selected any products.'),
                    //     });
                    // }
                     //else{
                        //if(lines.models.length > 0 && order.check_voucher_validy()) {
                        if(lines.models.length > 0) {
                            var product = self.pos.db.get_product_by_id(self.coupon_product);
                            var price = -1;
                            if (order.coupon_status['voucher_val_type'] == 'fix') {
                                price *= order.coupon_status['voucher_value'];
                            }
                            if (order.coupon_status['voucher_val_type'] == 'persen') {
                                price *= order.get_total_with_tax() * order.coupon_status['voucher_value'] / 100;
                            }   
                            if ((order.get_total_with_tax() + price) < 0) {
                                //self.gui.close_popup();
                                // self.gui.show_popup('error', {
                                //     'title': _t('Unable to apply coupon !'),
                                //     'body': _t('Coupon amount is too large to apply. The total amount cannot be negative'),
                                // });
                                price = order.get_total_with_tax() * -1 ; 
                            }
                        
                            order.add_product(product, {quantity: 1, price: price});
                            order.coupon_applied();

                            // Add History Faiz

                            var temp= {
                                'name': self.coupon_res[0]['name'],
                                'voucher_value': self.coupon_res[0]['voucher_value'],
                                'channel_used': self.coupon_res[0]['voucher_usage'],
                                'user_id': self.coupon_res[0]['customer_id'],
                                'voucher_id' : self.coupon_res[0]['id'],
                                'transaction_type': 'debit',
                                'state':'draft',
                                'description': self.coupon_res[0]['note'],
                            }
                            // self.pos.histo.push(temp);

                            new Model('history').call('create',[temp]);

                            // updating coupon balance after applying coupon
                            // var client = self.pos.get_client();
                            // var temp = {
                            //     'partner_id': client['id'],
                            //     'coupon_pos': order.coupon_status['voucher_code'],
                            // };
                            //new Model('partner.coupon.pos').call('update_history', ['', temp]).done(function (result) {
                                // alert("result")
                                // var applied = self.pos.coupons;
                                // var already_used = false;
                                // for (var j in applied) {
                                //     if (applied[j]['customer_id'][0] == client['id'] &&
                                //         applied[j]['voucher_code'] == order.coupon_status['voucher_code']) {
                                //         // applied[j]['number_pos'] += 1;
                                //         already_used = true;
                                //         break;
                                //     }
                                // }
                                // if (!already_used) {
                                //     var temp = {
                                //         'partner_id': [client['id'], client['name']],
                                //         'number_pos': 1,
                                //         'coupon_pos': order.coupon_status['code']
                                //     };
                                //     self.pos.applied_coupon.push(temp);
                                // }
                            //});
                            self.gui.close_popup();
                    
                        }
                        else{
                            self.gui.close_popup();
                            self.gui.show_popup('error',{
                                'title': _t('Unable to apply coupon !'),
                                'body': _t('This coupon is not applicable on the products or category you have selected !'),
                            });
                        }
                    //}
                }
                else{
                    self.gui.close_popup();
                    self.gui.show_popup('error',{
                        'title': _t('Unable to apply coupon !'),
                        'body': _t('Invalid Code or no Coupons left !'),
                    });
                }
            });
        },
    });
    gui.define_popup({name:'coupon', widget: CouponPopupWidget});

// screens.define_action_button({
//     'name': 'voucher_button',
//     'widget': VoucherButton,
// });



});
