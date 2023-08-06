Blockly.Blocks.python_file_open= {
    init: function() {
    this.appendDummyInput()
        .appendField("打开文件");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("模式")
        .appendField(new Blockly.FieldDropdown([["r","r"],["rb","rb"],["r+","r+"],["rb+","rb+"],["w","w"],["wb","wb"],["w+","w+"],["wb+","wb+"],["a","a"],["ab","ab"],["a+","a+"],["ab+","ab+"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("打开文件");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_file_open_msg= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获得");
    this.appendDummyInput()
        .appendField("的")
        .appendField(new Blockly.FieldDropdown([["文件名","name"],["是否已关闭","closed"],["访问模式","mode"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("获取打开文件的信息");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_file_close= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("关闭");
    this.appendDummyInput()
        .appendField("文件");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("关闭文件");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_file_write= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("文件");
    this.appendValueInput("TXT")
        .setCheck(null)
        .appendField(" 写入内容");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("写入内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_file_read= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("读取");
    this.appendDummyInput()
        .appendField("文件")
        .appendField(new Blockly.FieldDropdown([["全部","read"],["一行","readline"],["所有行","readlines"]]), "V")
        .appendField("内容");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("读取文件内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_time= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取")
        .appendField(new Blockly.FieldDropdown([["年","0"],["月","1"],["日","2"],["小时","3"],["分钟","4"],["秒","5"],["一周的第几日","6"],["	一年的第几日","7"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("获取时间");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_time_time= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取当前时间戳");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("获取时间戳,1970纪元后经过的浮点秒数");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_requests_null= {
    init: function() {
    this.appendDummyInput()
        .appendField("发送")
        .appendField(new Blockly.FieldDropdown([["get","get"],["post","post"],["put","put"],["delete","delete"],["head","head"],["options","options"]]), "V");
    this.appendValueInput("URL")
        .setCheck(String)
        .appendField("网络请求到");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("发送网络请求，获取返回数据");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_requests_params= {
    init: function() {
    this.appendDummyInput()
        .appendField("发送")
        .appendField(new Blockly.FieldDropdown([["get","get"],["post","post"],["put","put"],["delete","delete"],["head","head"],["options","options"]]), "V");
    this.appendValueInput("PAR")
        .setCheck(null)
        .appendField(" 参数");
    this.appendValueInput("URL")
        .setCheck(String)
        .appendField("网络请求到");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("发送带参数的网络请求，获取返回数据");
    this.setHelpUrl("");
    }
  };
  
  Blockly.Blocks.python_requests_read= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取");
    this.appendValueInput("DATA")
        .setCheck(null);
    this.appendDummyInput()
        .appendField(" 的")
        .appendField(new Blockly.FieldDropdown([["响应文本","text"],["JSON格式的内容","json()"],["响应状态码","status_code"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("获取返回内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_requests_set_encoding= {
    init: function() {
    this.appendDummyInput()
        .appendField("设置");
    this.appendValueInput("DATA")
        .setCheck(null);
    this.appendDummyInput()
        .appendField(" 的编码为");
    this.appendValueInput("V")
        .setCheck(String);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("设置编码格式");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.mxpi_url= {
    init: function() {
    this.appendDummyInput()
        .appendField("文件系统路径");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('neizhi_blocks');
    this.setTooltip("文件系统路径");
    this.setHelpUrl("");
    }
  };