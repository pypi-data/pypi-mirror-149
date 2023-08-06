Blockly.Python.baiduAI_init=function(a){
    Blockly.Python.definitions_['MxbaiduAi_init'] = 'from Mx import image';
    var app_id = Blockly.Python.valueToCode(this,'APP_ID',Blockly.Python.ORDER_ASSIGNMENT);
    var api_key = Blockly.Python.valueToCode(this,'API_KEY',Blockly.Python.ORDER_ASSIGNMENT);
    var api_sckey = Blockly.Python.valueToCode(this,'API_SCKEY',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'image.imageAI('+app_id+','+api_key+','+api_sckey+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.baiduAI_image=function(a){
    var v = Blockly.Python.valueToCode(this,'V',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var model = this.getFieldValue('MOEDL')
    var code= v+'.'+model+'('+img+')\n'
    return code;
}

Blockly.Python.baiduAI_result=function(a){
    var v = Blockly.Python.valueToCode(this,'V',Blockly.Python.ORDER_ASSIGNMENT);
    var code = v+'.result()'
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.baiduAI_asr=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var file = Blockly.Python.valueToCode(this,'FILE',Blockly.Python.ORDER_ASSIGNMENT);
    var sd = Blockly.Python.valueToCode(this,'SD',Blockly.Python.ORDER_ASSIGNMENT);
    var dev = this.getFieldValue('DEV')
    var code= name+'.asr('+file+','+sd+','+dev+')\n'
    return code;
}

Blockly.Python.baiduAI_synthesis=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var text = Blockly.Python.valueToCode(this,'TEXT',Blockly.Python.ORDER_ASSIGNMENT);
    var spd = Blockly.Python.valueToCode(this,'SPD',Blockly.Python.ORDER_ASSIGNMENT);
    var pit = Blockly.Python.valueToCode(this,'PIT',Blockly.Python.ORDER_ASSIGNMENT);
    var vol = Blockly.Python.valueToCode(this,'VOL',Blockly.Python.ORDER_ASSIGNMENT);
    var file = Blockly.Python.valueToCode(this,'FILE',Blockly.Python.ORDER_ASSIGNMENT);
    var per = this.getFieldValue('PER')
    var code= name+'.synthesis('+text+','+spd+','+pit+','+vol+','+per+','+file+')\n'
    return code;
}
