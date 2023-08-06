Blockly.Python.display_max7219_init = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    var w = this.getFieldValue('W');
    var h = this.getFieldValue('H');
    var wn = this.getFieldValue('WN');
    var hn = this.getFieldValue('HN');
    var p = this.getFieldValue('P');
    var code = 'max7219.led_init('+w+','+h+','+wn+','+hn+','+p+')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python.display_max7219_point = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var list =  Blockly.Python.valueToCode(this, 'LIST', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.point('+list+')\n';
    return code;
};

Blockly.Python.display_max7219_line = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var list =  Blockly.Python.valueToCode(this, 'LIST', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.line('+list+')\n';
    return code;
};

Blockly.Python.display_max7219_contrast = function () {
  var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
  var num =  Blockly.Python.valueToCode(this, 'NUM', Blockly.Python.ORDER_ATOMIC);
  var code = name+'.contrast('+num+')\n';
  return code;
};

Blockly.Python.display_max7219_show = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.show()\n';
    return code;
};

Blockly.Python.display_max7219_text = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    Blockly.Python.definitions_['MAX7219_font'] = 'from Mx.core.legacy import font';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text =  Blockly.Python.valueToCode(this, 'TEXT', Blockly.Python.ORDER_ATOMIC);
    var xy =  Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var font = this.getFieldValue('FONT');
    var code = name+'.texts('+text+','+xy+',font.'+font+')\n';
    return code;
};

Blockly.Python.display_max7219_gtext = function () {
    Blockly.Python.definitions_['MAX7219'] = 'from Mx import max7219';
    Blockly.Python.definitions_['MAX7219_font'] = 'from Mx.core.legacy import font';
    var name =  Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var text =  Blockly.Python.valueToCode(this, 'TEXT', Blockly.Python.ORDER_ATOMIC);
    var sp = this.getFieldValue('SP');
    var font = this.getFieldValue('FONT');
    var code = name+'.show_text('+text+',font.'+font+','+sp+')\n';
    return code;
};

Blockly.Python.display_oled_init = function() {
    Blockly.Python.definitions_['OLED'] = 'from Mx import oleds';
    var name = this.getFieldValue('NAME');
    var w = this.getFieldValue('W');
    var h = this.getFieldValue('H');
    var port = this.getFieldValue('PORT');
    var addr= this.getFieldValue('ADDR');
    var color = this.getFieldValue('COLOR');
    var code = 'oleds.i2c_init(\"'+name+'\",'+addr+','+port+',\"'+color+'\",w='+w+',h='+h+')';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python.display_oled_text = function() {
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var xy = Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var txt = Blockly.Python.valueToCode(this, 'TXT', Blockly.Python.ORDER_ATOMIC);
    var color = this.getFieldValue('COLOR');
    var font = this.getFieldValue('FONT');
    var font_size = this.getFieldValue('FONTSIZE');
    var code = name+'.texts('+xy+','+txt+',\"'+color+'\",\"'+font+'\",'+font_size+')\n';
    return code;
  };

  Blockly.Python.display_oled_ellipse = function() {
    var name= Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var xy = Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var color = this.getFieldValue('COLOR');
    var colors = this.getFieldValue('COLORS');
    var code = name+'.ellipse('+xy+',\"'+color+'\",\"'+colors+'\")\n';
    return code;
  };

  Blockly.Python.display_oled_rect = function() {
    var name= Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var xy = Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var color = this.getFieldValue('COLOR');
    var colors = this.getFieldValue('COLORS');
    var code = name+'.rect('+xy+',\"'+color+'\",\"'+colors+'\")\n';
    return code;
  };

  Blockly.Python.display_oled_polygon = function() {
    var name= Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var xy = Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var color = this.getFieldValue('COLOR');
    var colors = this.getFieldValue('COLORS');
    var code = name+'.polygon('+xy+',\"'+color+'\",\"'+colors+'\")\n';
    return code;
  };

  Blockly.Python.display_oled_line = function() {
    var name= Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var xy = Blockly.Python.valueToCode(this, 'XY', Blockly.Python.ORDER_ATOMIC);
    var color = this.getFieldValue('COLOR');
    var code = name+'.line('+xy+',\"'+color+'\")\n';
    return code;
  };
  
  Blockly.Python.display_oled_show = function() {
    var name= Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.show()\n';
    return code;
  };

  Blockly.Python.display_oled_horizontal_scroll = function() {
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var txt = Blockly.Python.valueToCode(this, 'TXT', Blockly.Python.ORDER_ATOMIC);
    var v = this.getFieldValue('V');
    var font = this.getFieldValue('FONT');
    var font_size = this.getFieldValue('FONTSIZE');
    var code = name+'.horizontal_scroll('+txt+','+v+',\"'+font+'\",'+font_size+')\n';
    return code;
  };

  Blockly.Python.display_oled_vertical_scroll = function() {
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var txt = Blockly.Python.valueToCode(this, 'TXT', Blockly.Python.ORDER_ATOMIC);
    var v = this.getFieldValue('V');
    var font = this.getFieldValue('FONT');
    var font_size = this.getFieldValue('FONTSIZE');
    var code = name+'.vertical_scroll('+txt+','+v+',\"'+font+'\",'+font_size+')\n';
    return code;
  };

  Blockly.Python.display_oled_display_img = function() {
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var url = Blockly.Python.valueToCode(this, 'URL', Blockly.Python.ORDER_ATOMIC);
    var w = Blockly.Python.valueToCode(this, 'W', Blockly.Python.ORDER_ATOMIC);
    var h = Blockly.Python.valueToCode(this, 'H', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.display_img('+url+','+w+','+h+')\n';
    return code;
  };

  Blockly.Python.display_oled_clear = function() {
    var name = Blockly.Python.valueToCode(this, 'NAME', Blockly.Python.ORDER_ATOMIC);
    var code = name+'.clear()\n';
    return code;
  };