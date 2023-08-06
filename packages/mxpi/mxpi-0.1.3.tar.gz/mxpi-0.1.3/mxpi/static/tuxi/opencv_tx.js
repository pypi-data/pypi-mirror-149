Blockly.Blocks.python_opencv_imread= {
    init: function() {
    this.appendDummyInput()
        .appendField("以")
        .appendField(new Blockly.FieldDropdown([["彩色图像","1"],["灰度图像","0"]]), "V")
        .appendField("模式");
    this.appendValueInput("NAME")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("读取图片");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("opencv读取图像");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_imshow= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("创建窗口");
    this.appendValueInput("IMG")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField(" 显示图片");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("opencv创建窗口显示图片");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_waitKey= {
    init: function() {
    this.appendDummyInput()
        .appendField("等待用户按键并返回按键ASCII值");
    this.appendValueInput("TIME")
        .setCheck(Number)
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("等待时间");
    this.appendDummyInput()
        .appendField("ms");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("等待用户按键并返回按键ASCII值");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_imwrite= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("保存图像");
    this.appendValueInput("URL")
        .setCheck(String)
        .appendField("到");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("保存图像");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_roi= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("拷贝图像");
    this.appendValueInput("X")
        .setCheck(Number)
        .appendField("区域")
        .appendField("x");
    this.appendValueInput("Y")
        .setCheck(Number)
        .appendField("y");
    this.appendValueInput("W")
        .setCheck(Number)
        .appendField("w");
    this.appendValueInput("H")
        .setCheck(Number)
        .appendField("h");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("获取部分区域图像");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_shape= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取图像");
    this.appendDummyInput()
        .appendField(" 的")
        .appendField(new Blockly.FieldDropdown([["高","0"],["宽","1"],["通道数","2"]]), "V");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("获取图像的高、宽和通道数");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_resize= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("缩放图像");
    this.appendValueInput("W")
        .setCheck(Number)
        .appendField("宽");
    this.appendValueInput("H")
        .setCheck(Number)
        .appendField("高");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("按比例缩放图像");
    this.setHelpUrl("");
    }
  };


  Blockly.Blocks.python_opencv_color_block= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("对图像");
    this.appendValueInput("COLOR")
        .setCheck(null)
        .appendField("进行色块识别 参数");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("对图像进行色块识别,参数为HSV颜色区域( h_min , h_max , s_min , s_max , v_min , v_max ))");
    this.setHelpUrl("");
    }
  };


  Blockly.Blocks.python_opencv_rectangle= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("在图像");
    this.appendValueInput("RECT")
        .setCheck(null)
        .appendField("上绘制矩形(x,y,w,h)");
    this.appendDummyInput()
        .appendField(" 颜色")
        .appendField(new Blockly.FieldColour("#33cc00"), "COLOR")
        .appendField(" 粗细")
        .appendField(new Blockly.FieldNumber(2, -1, 10000, 1), "SIZE");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("在图像上绘制矩形");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_opencam= {
    init: function() {
    this.appendDummyInput()
        .appendField("打开摄像头");
    this.appendValueInput("NAME")
        .setCheck(Number)
        .appendField(" ID");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("opencv打开摄像头");
    this.setHelpUrl("");
    }
  };
  
  Blockly.Blocks.python_opencv_readcam= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取摄像头");
    this.appendDummyInput()
        .appendField("当前帧");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("opencv打开摄像头");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_circle= {
    init: function() {
    this.appendValueInput("IMG")
        .setCheck(null)
        .appendField("在图像");
    this.appendValueInput("XY")
        .setCheck(null)
        .appendField("上绘制圆 圆心(x,y)");
    this.appendValueInput("RAD")
        .setCheck(null)
        .appendField(" 半径");
    this.appendDummyInput()
        .appendField(" 颜色")
        .appendField(new Blockly.FieldColour("#ff9900"), "COLOR")
        .appendField(" 填充")
        .appendField(new Blockly.FieldDropdown([["是","-1"],["否","1"]]), "TK");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("在图像上绘制圆");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_line= {
    init: function() {
    this.appendValueInput("IMG")
        .setCheck(null)
        .appendField("在图像");
    this.appendValueInput("STXY")
        .setCheck(null)
        .appendField("上绘制直线  起点");
    this.appendValueInput("ENDXY")
        .setCheck(null)
        .appendField("终点");
    this.appendDummyInput()
        .appendField(new Blockly.FieldColour("#ff9900"), "COLOR");
    this.appendValueInput("SIZE")
        .setCheck(null)
        .appendField("粗细");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("在图像上绘制直线");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.opencv_find_camid= {
    init: function() {
    this.appendDummyInput()
        .appendField("扫描可用摄像头ID");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("检查摄像头id");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.python_opencv_text= {
    init: function() {
    this.appendValueInput("IMG")
        .setCheck(null)
        .appendField("在图像");
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField("上绘制文字");
    this.appendValueInput("XY")
        .setCheck(null)
        .appendField("坐标(x,y)");
    this.appendValueInput("FONTS")
        .setCheck(null)
        .appendField("字体大小");
    this.appendDummyInput()
        .appendField("颜色")
        .appendField(new Blockly.FieldColour("#ff0000"), "COLOR");
    this.appendValueInput("SIZE")
        .setCheck(null)
        .appendField("粗细");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('OpenCV_blocks');
    this.setTooltip("在图像上绘制文字");
    this.setHelpUrl("");
    }
  };