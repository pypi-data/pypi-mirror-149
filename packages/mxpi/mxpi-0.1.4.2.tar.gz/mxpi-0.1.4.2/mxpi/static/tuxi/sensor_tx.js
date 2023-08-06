
  Blockly.Blocks.sensor_dht_init= {
    init: function() {
    this.appendDummyInput()
        .appendField(" 初始化")
        .appendField(new Blockly.FieldDropdown([["DHT11","DHT11"],["DHT22","DHT22"],["AM2302","AM2302"]]), "NAME");
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField(" 引脚(BCM)");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sensor_blocks');
    this.setTooltip("获取温湿度传感器的数值");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sensor_dht_read= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取温湿度传感器的");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("")
        .appendField(new Blockly.FieldDropdown([["温度","1"],["湿度","0"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sensor_blocks');
    this.setTooltip("初始化超声波测距模块(HC-SR04)");
    this.setHelpUrl("");
    }
  };
  Blockly.Blocks.sensor_hcsr04= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化超声波测距");
    this.appendValueInput("TRIG")
        .setCheck(null)
        .appendField("Trig#");
    this.appendValueInput("ECHO")
        .setCheck(null)
        .appendField("Echo#");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sensor_blocks');
    this.setTooltip("初始化超声波测距模块(HC-SR04)");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sensor_hcsr04_read= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取超声波传感器");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("的值(cm)");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sensor_blocks');
    this.setTooltip("初始化超声波测距模块(HC-SR04)");
    this.setHelpUrl("");
    }
  };
