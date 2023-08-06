Blockly.Blocks.baiduAI_init= {
    init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("初始化百度AI");
    this.appendValueInput("APP_ID")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" APP_ID");
    this.appendValueInput("API_KEY")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" APIKey");
    this.appendValueInput("API_SCKEY")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" SecretKey");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("初始化百度AI");
    this.setHelpUrl("");
    }
  };


  
  Blockly.Blocks.baiduAI_image= {
    init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("调用");
    this.appendValueInput("V")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT);
    this.appendValueInput("IMG")
        .setCheck(String)
        .appendField("对图片");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("进行")
        .appendField(new Blockly.FieldDropdown([["通用场景识别","advancedGeneral"],["图像主题检测","objectDetect"],["菜品识别","dishDetect"],["商标识别","logoSearch"],["动物识别","animalDetect"],["植物识别","plantDetect"],["地标识别","landmark"],["果蔬识别","ingredient"],["货币识别","currency"],["车辆识别","carDetect"]]), "MOEDL");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("进行百度AI识别");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.baiduAI_result= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取");
    this.appendValueInput("V")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("识别结果");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("获取图像识别结果");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.baiduAI_asr= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("调用");
    this.appendValueInput("FILE")
        .setCheck(null)
        .appendField("对音频");
    this.appendValueInput("SD")
        .setCheck(null)
        .appendField("采样率");
    this.appendDummyInput()
        .appendField("进行识别  语言")
        .appendField(new Blockly.FieldDropdown([["普通话(纯中文识别)","1537"],["普通话远场","1936"],["英语","1737"],["粤语","1637"],["四川话","1837"]]), "DEV");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("BaiduAI短语音识别");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.baiduAI_synthesis= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("调用");
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField("语音合成 ");
    this.appendValueInput("SPD")
        .setCheck(null)
        .appendField("语速(0-9)");
    this.appendValueInput("PIT")
        .setCheck(null)
        .appendField("语调(0-9)");
    this.appendValueInput("VOL")
        .setCheck(null)
        .appendField("音量(0-15)");
    this.appendDummyInput()
        .appendField("发音人")
        .appendField(new Blockly.FieldDropdown([["度小美","0"],["度小宇","1"],["度逍遥","3"],["度丫丫","4"],["度小娇","5"],["度小萌","111"],["度米朵","103"],["度小童","110"],["度博文","106"],["度小鹿","5118"],["度逍遥(精品)","5003"]]), "PER");
    this.appendValueInput("FILE")
        .setCheck(null)
        .appendField("输出到文件");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("进行语音合成");
    this.setHelpUrl("");
    }
  };
