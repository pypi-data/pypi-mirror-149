Blockly.Python.pins = function() {
    var code = this.getFieldValue('PIN');
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python.pins_ad = function() {
    var code = this.getFieldValue('PIN');
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

Blockly.Python.inout_highlow = function () {
    // Boolean values HIGH and LOW.
    var code = (this.getFieldValue('BOOL') == 'HIGH') ? 'HIGH' : 'LOW';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_model'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var model = this.getFieldValue('MODEL')
    var code = 'GPIO.setmode(GPIO.'+ model + ')\n';
    return code;
};

Blockly.Python['GPIO_getmode'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    Blockly.Python.definitions_['var_declare_'+'NAME'] = 'sss';
    var code = 'GPIO.getmode()';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_setup'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var model = this.getFieldValue('MODEL');
    var code = 'GPIO.setup('+pin+', GPIO.'+model+')\n';
    return code;
};

Blockly.Python['GPIO_out'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var model = Blockly.Python.valueToCode(this, 'STAT', Blockly.Python.ORDER_ATOMIC);
    var code = 'GPIO.output('+pin+', GPIO.'+model+')\n';
    return code;
};

Blockly.Python['GPIO_in'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var code = 'GPIO.input('+pin+')\n';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_pwm_init'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var hz =  Blockly.Python.valueToCode(this, 'HZ', Blockly.Python.ORDER_ATOMIC);
    var code ='GPIO.PWM('+pin+', '+hz+') ';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_pwm_start'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var dc =  Blockly.Python.valueToCode(this, 'DC', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.start('+dc+')\n'
    return code;
};

Blockly.Python['GPIO_pwm_ChangeFrequency'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var hz =  Blockly.Python.valueToCode(this, 'HZ', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.ChangeFrequency('+hz+')\n'
    return code;
};

Blockly.Python['GPIO_pwm_ChangeDutyCycle'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var dc =  Blockly.Python.valueToCode(this, 'DC', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.ChangeDutyCycle('+dc+')\n'
    return code;
};

Blockly.Python['serial_init'] = function () {
    Blockly.Python.definitions_['serial'] = 'import serial';
    var port =  this.getFieldValue('NAME');
    var bd =  Blockly.Python.valueToCode(this, 'BD', Blockly.Python.ORDER_ATOMIC);
    var time =  Blockly.Python.valueToCode(this, 'TIME', Blockly.Python.ORDER_ATOMIC);
    var code ='serial.Serial(port="/dev/'+port+'", baudrate='+bd+', timeout='+time+')'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_write'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text =  Blockly.Python.valueToCode(this, 'TEXT', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.write('+text+'.encode("gbk"))\n'
    return code;
};

Blockly.Python['serial_read'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var num =  Blockly.Python.valueToCode(this, 'NUM', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.read('+num+').decode("utf-8")'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_readline'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.readline().decode("utf-8")'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_inWaiting'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.in_waiting'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_outWaiting'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.out_waiting'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_flush'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.flush()\n'
    return code;
};

Blockly.Python['serial_readable'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.readable()'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_writable'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.writable()'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['serial_get_settings'] = function () {
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.get_settings()'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_AD_init'] = function () {
    Blockly.Python.definitions_['AD_init'] = 'from Mx import PCF8591';
    var code ='PCF8591.init()'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_AD_init'] = function () {
    Blockly.Python.definitions_['AD_init'] = 'from Mx import PCF8591';
    var code ='PCF8591.init()'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_AD_IN'] = function () {
    Blockly.Python.definitions_['AD_init'] = 'from Mx import PCF8591';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.read("'+pin+'")'
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_AD_OUT'] = function () {
    Blockly.Python.definitions_['AD_init'] = 'from Mx import PCF8591';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var val =  Blockly.Python.valueToCode(this, 'VAR', Blockly.Python.ORDER_ATOMIC);
    var code =name+'.write('+val+')\n'
    return code;
};

