
Blockly.Python.Servo_init=function(a){
    Blockly.Python.definitions_['Servo'] = 'from Mx import Servo';
    var pin = Blockly.Python.valueToCode(this,'PIN',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'Servo.gs90('+pin+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.Servo_turn=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var jd = Blockly.Python.valueToCode(this,'JD',Blockly.Python.ORDER_ASSIGNMENT);
    var time = Blockly.Python.valueToCode(this,'TIME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.turn('+jd+','+time+')\n';
    return code;
}


Blockly.Python.sound_play=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var fs = Blockly.Python.valueToCode(this,'FS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'sound.play('+name+','+fs+')\n';
    return code;
}

Blockly.Python.sound_stop=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var fs = Blockly.Python.valueToCode(this,'FS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'sound.stop()\n';
    return code;
}

Blockly.Python.sound_record=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var file = Blockly.Python.valueToCode(this,'FILE',Blockly.Python.ORDER_ASSIGNMENT);
    var s = Blockly.Python.valueToCode(this,'S',Blockly.Python.ORDER_ASSIGNMENT);
    var fd = Blockly.Python.valueToCode(this,'FD',Blockly.Python.ORDER_ASSIGNMENT);
    var ch = Blockly.Python.valueToCode(this,'CHAN',Blockly.Python.ORDER_ASSIGNMENT);
    var msg = this.getFieldValue('MSG')
    var code= 'sound.record('+file+','+s+','+fd+','+ch+','+msg+')\n';
    return code;
}

Blockly.Python.sound_query_devices=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var code= 'sound.query_devices()';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.sound_getSaRa=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var file = Blockly.Python.valueToCode(this,'FILE',Blockly.Python.ORDER_ASSIGNMENT);
    var model = this.getFieldValue('MODEL')
    var code= 'sound.SaRa('+file+')['+model+']';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.sound_resample_rate=function(a){
    Blockly.Python.definitions_['sound'] = 'from Mx import sound';
    var file = Blockly.Python.valueToCode(this,'FILE',Blockly.Python.ORDER_ASSIGNMENT);
    var sd = Blockly.Python.valueToCode(this,'SD',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'sound.resample_rate('+file+','+sd+')\n';
    return code;
}