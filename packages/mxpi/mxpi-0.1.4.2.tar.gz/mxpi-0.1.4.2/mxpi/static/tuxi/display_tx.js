Blockly.Blocks.display_max7219_init= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化MAX7219");
    this.appendDummyInput()
        .appendField("宽")
        .appendField(new Blockly.FieldNumber(8, 1, 10000, 1), "W");
    this.appendDummyInput()
        .appendField(" 高")
        .appendField(new Blockly.FieldNumber(8, 1, 10000, 1), "H");
    this.appendDummyInput()
        .appendField(" 水平个数")
        .appendField(new Blockly.FieldNumber(1, 1, 10000, 1), "WN");
    this.appendDummyInput()
        .appendField(" 垂直个数")
        .appendField(new Blockly.FieldNumber(1, 1, 10000, 1), "HN");
    this.appendDummyInput()
        .appendField(" 旋转")
        .appendField(new Blockly.FieldDropdown([["0°","0"],["90°","90"],["-90°","-90"],["180°","180"]]), "P");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("初始化MAX7219");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_point= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField(" 点亮");
    this.appendValueInput("LIST")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("MAX7219点亮单个LED");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_show= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("显示");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("MAX7219点亮单个LED");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_line= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField(" 点亮");
    this.appendValueInput("LIST")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("MAX7219点亮直线");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_text= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendValueInput("XY")
        .setCheck(null)
        .appendField(" 在坐标(xy)");
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField(" 显示");
    this.appendDummyInput()
        .appendField(" 字体")
        .appendField(new Blockly.FieldDropdown([["LCD_FONT","LCD_FONT"],["CP437_FONT","CP437_FONT"],["ATARI_FONT","ATARI_FONT"],["SEG7_FONT","SEG7_FONT"],["SINCLAIR_FONT","SINCLAIR_FONT"],["SPECCY_FONT","SPECCY_FONT"],["TINY_FONT","TINY_FONT"],["UKR_FONT","UKR_FONT"]]), "FONT");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("MAX7219显示文字");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_gtext= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField(" 滚动显示");
    this.appendDummyInput()
        .appendField(" 速度")
        .appendField(new Blockly.FieldNumber(0.05, 0, 1000, 0.01), "SP");
    this.appendDummyInput()
        .appendField("秒  字体")
        .appendField(new Blockly.FieldDropdown([["LCD_FONT","LCD_FONT"],["CP437_FONT","CP437_FONT"],["ATARI_FONT","ATARI_FONT"],["SEG7_FONT","SEG7_FONT"],["SINCLAIR_FONT","SINCLAIR_FONT"],["SPECCY_FONT","SPECCY_FONT"],["TINY_FONT","TINY_FONT"],["UKR_FONT","UKR_FONT"]]), "FONT");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("MAX7219显示文字");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_max7219_contrast= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendValueInput("NUM")
        .setCheck(Number)
        .appendField("调整亮度(0~255)");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("调整亮度");
    this.setHelpUrl("");
    }
  };
  Blockly.Blocks.display_oled_init= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化")
        .appendField(new Blockly.FieldDropdown([["ssd1306","ssd1306"],["ssd1325","ssd1325"],["ssd1331","ssd1331"],["sh1106","sh1106"]]), "NAME")
        .appendField("宽")
        .appendField(new Blockly.FieldNumber(128, 0, 10000, 1), "W")
        .appendField("高")
        .appendField(new Blockly.FieldNumber(64, 0, 10000, 1), "H")
        .appendField("端口")
        .appendField(new Blockly.FieldDropdown([["1","1"],["0","0"]]), "PORT")
        .appendField("地址")
        .appendField(new Blockly.FieldTextInput("0x3C"), "ADDR")
        .appendField("背景颜色")
        .appendField(new Blockly.FieldColour("#000000"), "COLOR");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("初始化OLED显示屏");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_text= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("XY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("在(x,y)");
    this.appendValueInput("TXT")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("显示");
    this.appendDummyInput()
        .appendField("颜色")
        .appendField(new Blockly.FieldColour("#ffffff"), "COLOR");
    this.appendDummyInput()
        .appendField("字体")
        .appendField(new Blockly.FieldDropdown([["微软雅黑","font/msyh.ttc"],["微软雅黑粗体","font/msyhbd.ttc"],["Sitka","font/Sitka.ttc"]]), "FONT")
        .appendField("字体大小")
        .appendField(new Blockly.FieldNumber(12, 0, 100000, 1), "FONTSIZE");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("在OLED上显示文字");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_ellipse= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("XY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("在(x,y,x,y)处");
    this.appendDummyInput()
        .appendField("画椭圆")
        .appendField("线条颜色")
        .appendField(new Blockly.FieldColour("#ffffff"), "COLOR")
        .appendField("填充颜色")
        .appendField(new Blockly.FieldColour("#000000"), "COLORS");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("画椭圆");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_rect= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("XY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("在(x,y,x,y)处");
    this.appendDummyInput()
        .appendField("画矩形")
        .appendField("线条颜色")
        .appendField(new Blockly.FieldColour("#ffffff"), "COLOR")
        .appendField("填充颜色")
        .appendField(new Blockly.FieldColour("#000000"), "COLORS");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("画矩形");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_polygon= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("XY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("在(x,y,x,y,x,y)处");
    this.appendDummyInput()
        .appendField("画三角形")
        .appendField("线条颜色")
        .appendField(new Blockly.FieldColour("#ffffff"), "COLOR")
        .appendField("填充颜色")
        .appendField(new Blockly.FieldColour("#000000"), "COLORS");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("画三角形");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_line= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("XY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("在(x,y,x,y)处");
    this.appendDummyInput()
        .appendField("画直线")
        .appendField("线条颜色")
        .appendField(new Blockly.FieldColour("#ffffff"), "COLOR")
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("画三角形");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_show= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendDummyInput()
        .appendField("显示画面");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("显示所画图像");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_horizontal_scroll= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("TXT")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("水平滚动显示内容");
    this.appendDummyInput()
        .appendField("滚动速度(1~100)")
        .appendField(new Blockly.FieldNumber(100, 1, 100, 1), "V");
    this.appendDummyInput()
        .appendField("字体")
        .appendField(new Blockly.FieldDropdown([["微软雅黑","font/msyh.ttc"],["微软雅黑粗体","font/msyhbd.ttc"],["Sitka","font/Sitka.ttc"]]), "FONT")
    this.appendDummyInput()
        .appendField("字体大小")
        .appendField(new Blockly.FieldNumber(12, 0, 10000, 1), "FONTSIZE");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("水平滚动显示内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_vertical_scroll= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("TXT")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("垂直滚动显示内容");
    this.appendDummyInput()
        .appendField("滚动速度(1~100)")
        .appendField(new Blockly.FieldNumber(100, 1, 100, 1), "V");
    this.appendDummyInput()
        .appendField("字体")
        .appendField(new Blockly.FieldDropdown([["微软雅黑","font/msyh.ttc"],["微软雅黑粗体","font/msyhbd.ttc"],["Sitka","font/Sitka.ttc"]]), "FONT")
    this.appendDummyInput()
        .appendField("字体大小")
        .appendField(new Blockly.FieldNumber(12, 0, 10000, 1), "FONTSIZE");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("垂直滚动显示内容");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_display_img= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendValueInput("URL")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("显示图片");
    this.appendValueInput("W")
        .setCheck(Number)
        .appendField("宽");
    this.appendValueInput("H")
        .setCheck(Number)
        .appendField("高");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("显示图片");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.display_oled_clear= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("擦除屏幕");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('display_blocks');
    this.setTooltip("擦除屏幕");
    this.setHelpUrl("");
    }
  };