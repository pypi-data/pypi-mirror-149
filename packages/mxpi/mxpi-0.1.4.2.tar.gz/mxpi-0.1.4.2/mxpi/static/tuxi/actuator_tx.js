Blockly.Blocks.Servo_init= {
    init: function() {
    this.appendValueInput("PIN")
        .setCheck(null)
        .appendField("初始化舵机  引脚#");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('actuator_blocks');
    this.setTooltip("初始化舵机");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Servo_turn= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("舵机");
    this.appendValueInput("JD")
        .setCheck(null)
        .appendField("角度(0~180)");
    this.appendValueInput("TIME")
        .setCheck(null)
        .appendField("延时(秒)");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('actuator_blocks');
    this.setTooltip("初始化舵机");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_play= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("播放");
    this.appendValueInput("FS")
        .setCheck(null)
        .appendField("比特率");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("播放wav文件");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_stop= {
    init: function() {
    this.appendDummyInput()
        .appendField("播放停止");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("停止播放");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_record= {
    init: function() {
    this.appendValueInput("FILE")
        .setCheck(null)
        .appendField("录制音频到");
    this.appendValueInput("S")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("录制(秒)");
    this.appendValueInput("FD")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("采样率");
    this.appendValueInput("CHAN")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("通道");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("输出结果")
        .appendField(new Blockly.FieldDropdown([["是","True"],["否","False"]]), "MSG");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("录制音频");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_query_devices= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取音频设备信息");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("获取音频设备信息");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_getSaRa= {
    init: function() {
    this.appendValueInput("FILE")
        .setCheck(null)
        .appendField("音频文件");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["采样率","0"],["时长","1"]]), "MODEL");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("获取音频文件采样率/时长");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.sound_resample_rate= {
    init: function() {
    this.appendValueInput("FILE")
        .setCheck(null)
        .appendField("修改音频文件");
    this.appendValueInput("SD")
        .setCheck(null)
        .appendField("采样率");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('sound_blocks');
    this.setTooltip("获取音频文件采样率/时长");
    this.setHelpUrl("");
    }
  };