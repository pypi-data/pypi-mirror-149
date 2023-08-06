Blockly.Blocks.yolo_fast_init= {
    init: function() {
    this.appendValueInput("MODEL")
        .setCheck(String)
        .appendField("初始化Yolo网络")
        .appendField("模型");
    this.appendValueInput("LABEL")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("标签");
    this.appendValueInput("ANCHOR")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Anchor");
    this.appendValueInput("OBJ")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("对象置信度");
    this.appendValueInput("CONF")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("种类置信度");
    this.appendValueInput("NMS")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Nms-iou");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化Yolo-Fast网络");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.yolo_fast_process= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("运行网络");
    this.appendValueInput("IMG")
        .setCheck(null)
        .appendField("推理图片");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("运行Yolo-Fast网络进行推理，返回识别结果");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.mp_face_detection= {
    init: function() {
    this.appendValueInput("VALUE")
        .setCheck(null)
        .appendField("初始化人脸检测网络")
        .appendField("阈值");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化MediaPipe进行人脸检测");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.mp_run= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("运行网络");
    this.appendValueInput("IMG")
        .setCheck(null)
        .appendField("推理图片");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("进行推理输出结果");
    this.setHelpUrl("");
    }
  };

  
  Blockly.Blocks.mp_face_mesh= {
    init: function() {
    this.appendValueInput("MAX")
        .setCheck(null)
        .appendField("初始化面网检测网络")
        .appendField("最大识别人脸数");
    this.appendValueInput("DETE")
        .setCheck(null)
        .appendField("检测阈值");
    this.appendValueInput("TRACK")
        .setCheck(null)
        .appendField("跟踪阈值");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化MediaPipe进行面部网格检测");
    this.setHelpUrl("https://gitcode.net/q924257/mediapipe-title/-/blob/master/face.png");
    }
  };

  Blockly.Blocks.mp_hands= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化手部检测网络");
    this.appendDummyInput()
        .appendField(" 模型复杂度")
        .appendField(new Blockly.FieldDropdown([["0","0"],["1","1"]]), "MODEL");
    this.appendValueInput("NUM")
        .setCheck(null)
        .appendField(" 手的数量");
    this.appendValueInput("DETE")
        .setCheck(null)
        .appendField(" 检测阈值");
    this.appendValueInput("TRACK")
        .setCheck(null)
        .appendField(" 跟踪阈值");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化MediaPipe进行手部检测");
    this.setHelpUrl("https://gitcode.net/q924257/mediapipe-title/-/blob/master/hand.png");
    }
  };

  Blockly.Blocks.mp_pose= {
    init: function() {
    this.appendDummyInput()
        .appendField("初始化人体姿态检测网络");
    this.appendDummyInput()
        .appendField(" 模型复杂度")
        .appendField(new Blockly.FieldDropdown([["0","0"],["1","1"],["2","2"]]), "MODEL");
    this.appendValueInput("DETE")
        .setCheck(null)
        .appendField(" 检测阈值");
    this.appendValueInput("TRACK")
        .setCheck(null)
        .appendField(" 跟踪阈值");
    this.appendValueInput("SEG")
        .setCheck(null)
        .appendField(" 分段阈值");
    this.appendValueInput("VIS")
        .setCheck(null)
        .appendField(" 检测范围");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化MediaPipe进行人体姿态检测");
    this.setHelpUrl("https://gitcode.net/q924257/mediapipe-title/-/blob/master/pose.png");
    }
  };

  Blockly.Blocks.audio_classify= {
    init: function() {
    this.appendValueInput("MODEL")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("初始化音频分类器 模型");
    this.appendValueInput("MAX")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("返回结果最大数量");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化音频分类器");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.audio_classify_run= {
    init: function() {
    this.appendValueInput("VAR")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("运行音频分类器");
    this.appendValueInput("WAV")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("推理音频");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("运行音频分类器推理音频,结果放回一个列表对象");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.SoundThread= {
    init: function() {
    this.appendValueInput("MODEL")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("初始化实时音频分类器 模型");
    this.appendValueInput("MAX")
        .setCheck(Number)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("返回最大结果数量");
    this.appendValueInput("SCORE")
        .setCheck(Number)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("阈值(0~1)");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("初始化实时音频分类器");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.SoundThread_get= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("获取实时音频分类器");
    this.appendDummyInput()
        .appendField("结果");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('AI_blocks');
    this.setTooltip("获取实时音频分类器结果");
    this.setHelpUrl("");
    }
  };


  