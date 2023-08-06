Blockly.Python.sensor_dht_init = function () {
    Blockly.Python.definitions_['Adafruit_DHT'] = 'import Adafruit_DHT';
    Blockly.Python.definitions_['Mx_dht'] = 'from Mx import DHT';
    var name = this.getFieldValue('NAME');
    var pin = Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var code = 'DHT.inits(Adafruit_DHT.'+name+','+pin+')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python.sensor_hcsr04 = function() {
    Blockly.Python.definitions_['hc-sr04'] = 'from Mx import hcsr04';
    var value_TRIG = Blockly.Python.valueToCode(this, 'TRIG', Blockly.Python.ORDER_ATOMIC);
    var value_ECHO = Blockly.Python.valueToCode(this, 'ECHO', Blockly.Python.ORDER_ATOMIC);
    var code = 'hcsr04.init('+value_TRIG+','+value_ECHO+')';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };


Blockly.Python.sensor_hcsr04_read = function() {
    var value_NAME = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code = value_NAME+'.read()';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

Blockly.Python.sensor_dht_read = function() {
    var value_NAME = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var v = this.getFieldValue('V');
    var code = value_NAME+'.read()['+v+']';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };