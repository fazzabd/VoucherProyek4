function pos_template_models(instance, module){
    //pos_base is instance.point_of_sale;

    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    // Add a model to load at POS start
    pos_base.PosModel.prototype.models.push({
        model: 'voucher',
        fields: ['name','voucher_code','expiry_date','voucher_val_type','voucher_value'],
        domain: null, //add a domain if wanted
        loaded: function(self,field){
            // Actions to do when the model has been loaded
           }
    });

    // Update existing model loader
    var models = pos_base.PosModel.prototype.models;
    for(var i=0; i<models.length; i++){
        var model=models[i];
        if(model.model === 'model.toupdate'){
             model.fields.push('field_to_add');
             // ....
        } 
    }

}