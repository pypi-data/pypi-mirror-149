
var pin =  [["0", "0"], ["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"], ["6", "6"], ["7", "7"], ["8", "8"], ["9", "9"], ["10", "10"], ["11", "11"], ["12", "12"], ["13", "13"], ["14", "14"], ["15", "15"], ["16", "16"], ["17", "17"], ["18", "18"], ["19", "19"], ["20", "20"], ["21", "21"], ["26", "26"], ["33", "33"], ["34", "34"], ["35", "35"], ["36", "36"], ["37", "37"], ["38", "38"], ["39", "39"], ["40", "40"]];
var pin_ad=[["A0","A0"],["A1","A2"],["A3","A3"],["A4","A4"]]

Blockly.Blocks['pins'] = {
    init: function() {
     this.setColour(90);
     this.appendDummyInput("")
     .appendField(new Blockly.FieldDropdown(pin), 'PIN');
     this.setOutput(true, Number);
   }
   };

   Blockly.Blocks['pins_ad'] = {
    init: function() {
     this.setColour(90);
     this.appendDummyInput("")
     .appendField(new Blockly.FieldDropdown(pin_ad), 'PIN');
     this.setOutput(true, Number);
   }
   };

Blockly.Blocks['inout_highlow'] = {
init: function() {
    this.setColour(90);
    this.appendDummyInput("")
    .appendField(new Blockly.FieldDropdown([['高', "HIGH"], ['低', "LOW"]]), 'BOOL')
    this.setOutput(true, Boolean);
    this.setTooltip();
}
};

Blockly.Blocks['GPIO_model'] = {
    /**
     * @this Blockly.Block
     */
     init: function() {
        this.appendDummyInput()
            .appendField("设置引脚编码方式为 ")
            .appendField(new Blockly.FieldDropdown([["BOARD","BOARD"],["BCM","BCM"]]), "MODEL")
        this.setInputsInline(false);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle('GPIO_blocks');
        this.setTooltip("设置引脚编号方式");
        this.setHelpUrl("");
        }
  };

  Blockly.Blocks['GPIO_getmode'] = {
    /**
     * @this Blockly.Block
     */
     init: function() {
        this.appendDummyInput()
            .appendField("当前引脚编号方式");
        this.setInputsInline(false);
        this.setOutput(true, null);
        this.setStyle('GPIO_blocks');
        this.setTooltip("获取当前引脚编号方式");
        this.setHelpUrl("");
        }
  };

  Blockly.Blocks['GPIO_setup'] = {
    /**
     * @this Blockly.Block
     */
     init: function() {
        this.appendValueInput("PIN", Number)
            .appendField("引脚 #")
            .setCheck(Number);
        this.appendDummyInput()
            .appendField(" 设为 ")
            .appendField(new Blockly.FieldDropdown([['输入','IN'],['输出','OUT']]),'MODEL');
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle('GPIO_blocks');
        this.setTooltip("设置引脚为输入/输出模式");
        this.setHelpUrl("");
        }
  };

  Blockly.Blocks['GPIO_out'] = {
    /**
     * @this Blockly.Block
     */
     init: function() {
        this.appendValueInput("PIN",Number)
            .setCheck(Number)
            .appendField("输出 引脚 #");
        this.appendValueInput('STAT')
            .setCheck(null)
            .appendField("赋值为")
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle('GPIO_blocks');
        this.setTooltip("设置引脚为输入/输出模式");
        this.setHelpUrl("");
        }
  };

  Blockly.Blocks['GPIO_in'] = {
    /**
     * @this Blockly.Block
     */
     init: function() {
        this.appendValueInput("PIN",Number)
            .setCheck(Number)
            .appendField("数字输入 引脚 #");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setStyle('GPIO_blocks');
        this.setTooltip("读取数字引脚的值");
        this.setHelpUrl("");
        }
  };

  Blockly.Blocks.GPIO_AD_IN= {
    init: function() {
    this.appendDummyInput()
        .appendField("模拟");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("输入 引脚 #");
    this.appendValueInput("PIN")
        .setCheck(null);
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("读取模拟引脚的值");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.GPIO_AD_init= {
    init: function() {
    this.appendDummyInput()
        .appendField("PCF8591数模转换模块初始化");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("初始化PCF8591数模转换模块");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.GPIO_AD_OUT= {
    init: function() {
    this.appendDummyInput()
        .appendField("模拟");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendValueInput("VAR")
        .setCheck(null)
        .appendField("输出值");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("模拟引脚输出值");
    this.setHelpUrl("");
    }
  };
  Blockly.Blocks.GPIO_pwm_init= {
    init: function() {
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField("创建PWM信号 引脚");
    this.appendValueInput("HZ")
        .setCheck(Number)
        .appendField("频率");
    this.appendDummyInput()
        .appendField("Hz");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("创建PWM信号");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.GPIO_pwm_start= {
    init: function() {
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField("启动 ");
    this.appendValueInput("DC")
        .setCheck(null)
        .appendField(" 占空比");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("启动PWM");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.GPIO_pwm_ChangeFrequency= {
    init: function() {
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField("更改 ");
    this.appendValueInput("HZ")
        .setCheck(null)
        .appendField(" 频率");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("更改PWM频率");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.GPIO_pwm_ChangeDutyCycle= {
    init: function() {
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField("更改 ");
    this.appendValueInput("DC")
        .setCheck(null)
        .appendField(" 占空比");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("更改PWM占空比");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_init= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化")
        .appendField(new Blockly.FieldDropdown([["Serial","ttyS0"],["Serial1","ttyAMA1"],["Serial2","ttyAMA2"],["Serial3","ttyAMA3"],["Serial4","ttyAMA4"]]), "NAME")
        .appendField("串口对象");
    this.appendValueInput("BD")
        .setCheck(null)
        .appendField("波特率");
    this.appendValueInput("TIME")
        .setCheck(null)
        .appendField("读取超时");
    this.appendDummyInput()
        .appendField("秒");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("初始化串口");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_write= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField("发送字符串");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("串口发送内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_read= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("读取字符串");
    this.appendValueInput("NUM")
        .setCheck(null)
        .appendField("字节数");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("读取串口数据");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_readline= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("读取字符串");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("读取串口数据");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_inWaiting= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取");
    this.appendDummyInput()
        .appendField("接收缓冲区中的字节数");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("获取接收缓冲区中的字节数");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_outWaiting= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取");
    this.appendDummyInput()
        .appendField("发送缓冲区中的字节数");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("获取发送缓冲区中的字节数");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_flush= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("清空缓冲区");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("清空缓冲区");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_readable= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("是否可读");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("串口是否可读");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_writable= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("是否可写");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("串口是否可写");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.serial_get_settings= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取");
    this.appendDummyInput()
        .appendField("设置参数");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('GPIO_blocks');
    this.setTooltip("获取串口参数字典");
    this.setHelpUrl("");
    }
  };
  

