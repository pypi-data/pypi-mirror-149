Blockly.Python.Blynk_init=function(a){
    Blockly.Python.definitions_['blynklib'] = 'import blynklib';
    var addr = Blockly.Python.valueToCode(this,'ADDR',Blockly.Python.ORDER_ASSIGNMENT);
    var post = Blockly.Python.valueToCode(this,'POST',Blockly.Python.ORDER_ASSIGNMENT);
    var api_sckey = Blockly.Python.valueToCode(this,'KEY',Blockly.Python.ORDER_ASSIGNMENT);
    var pr = Blockly.Python.valueToCode(this,'PR',Blockly.Python.ORDER_ASSIGNMENT);
    if(pr=='True'){
        var code= 'blynklib.Blynk('+api_sckey+',server='+addr+',port='+post+',log=print)';
    }
    else{
        var code= 'blynklib.Blynk('+api_sckey+',server='+addr+',port='+post+')';
    }
        return [code,Blockly.Python.ORDER_ATOMIC];
}


Blockly.Python.Blynk_run=function(a){
    Blockly.Python.definitions_['blynklib'] = 'import blynklib';
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run()\n';
    return code;
}

Blockly.Python.Blynk_connected=function(a){
    Blockly.Python.definitions_['blynklib'] = 'import blynklib';
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.connected()';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.blynk_iot_get_data = function () {
	var Vpin = this.getFieldValue('Vpin');
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
	var branch = Blockly.Python.statementToCode(this, 'STACK')|| '    pass\n';

	if (Blockly.Python.INFINITE_LOOP_TRAP) {
		branch = Blockly.Python.INFINITE_LOOP_TRAP.replace(/%1/g, '\'' + this.id + '\'') + branch;
	}
	var GetDataCode = "";
	if (this.arguments_.length == 1) {
		GetDataCode = ','+Blockly.Python.variableDB_.getName(this.arguments_[0], Blockly.Variables.NAME_TYPE);
	}
	else {
		for (var x = 0; x < this.arguments_.length; x++) {
			GetDataCode = GetDataCode + "," + Blockly.Python.variableDB_.getName(this.arguments_[x], Blockly.Variables.NAME_TYPE);
		}
	}
	var code = '@'+name+'.handle_event("write '+Vpin+'")\n' +
    'def write_virtual_pin_handler(blynk_pin'+GetDataCode+'):\n'+branch ;
	// var code =  'BLYNK_WRITE(' + Vpin+ ') {\n'+variable+" = param.as"+datatype+"();\n"+branch+'}\n';
	return code
};

Blockly.Python.blynk_iot_push_data = function () {
	var Vpin = this.getFieldValue('Vpin');
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
	var data = Blockly.Python.valueToCode(this, 'data', Blockly.Python.ORDER_ATOMIC);
	var code = name+'.virtual_write('+Vpin+','+data+')'+'\n';
	return code;
};

Blockly.Python.Blynk_iot_timer = function () {
	Blockly.Python.definitions_['BlynkTimer'] = 'import blynktimer\n'+
    'myTimerEvent=blynktimer.Timer()';
	var timerNo = this.getFieldValue('timerNo');
	var time = Blockly.Python.valueToCode(this, 'TIME', Blockly.Python.ORDER_ATOMIC);
	var funcName = 'myTimerEvent' + timerNo;
	var branch = Blockly.Python.statementToCode(this, 'DO') || '    pass\n';
	var code = '@myTimerEvent.register(vpin_num='+timerNo+', interval='+time/1000+', run_once=False)\n'+
    'def write_to_virtual_pin(vpin_num='+timerNo+'):\n'+branch;
	return code;
};

Blockly.Python.Blynk_time_run = function () {
	var code = 'myTimerEvent.run()\n';
	return code;
};

Blockly.Python.RGB_color_seclet = function() {
    var colour = this.getFieldValue('COLOR');
    var code='\''+colour+'\''
    return [code,Blockly.Python.ORDER_ATOMIC];
  };

Blockly.Python.Blynk_led = function() {
    var Vpin = this.getFieldValue('Vpin');
    var colour = Blockly.Python.valueToCode(this, 'COLOR', Blockly.Python.ORDER_ATOMIC);
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var pt = Blockly.Python.valueToCode(this, 'PT', Blockly.Python.ORDER_ATOMIC);
    var code=name+'.set_property('+Vpin+', "color",'+colour+')\n'+
             name+'.virtual_write('+Vpin+','+pt+')\n'
    return code;
  };

  Blockly.Python.Blynk_set_color = function() {
    var Vpin = this.getFieldValue('Vpin');
    var colour = Blockly.Python.valueToCode(this, 'COLOR', Blockly.Python.ORDER_ATOMIC);
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code=name+'.set_property('+Vpin+', "color",'+colour+')\n'
    return code;
  };