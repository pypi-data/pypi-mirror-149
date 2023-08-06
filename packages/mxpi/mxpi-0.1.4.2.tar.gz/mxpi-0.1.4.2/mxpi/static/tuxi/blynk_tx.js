
  //虚拟管脚选择
var BLYNK_VIRTUALPIN_SELECT = [
    ["V0", "V0"],
    ["V1", "V1"],
    ["V2", "V2"],
    ["V3", "V3"],
    ["V4", "V4"],
    ["V5", "V5"],
    ["V6", "V6"],
    ["V7", "V7"],
    ["V8", "V8"],
    ["V9", "V9"],
    ["V10", "V10"],
    ["V11", "V11"],
    ["V12", "V12"],
    ["V13", "V13"],
    ["V14", "V14"],
    ["V15", "V15"],
    ["V16", "V16"],
    ["V17", "V17"],
    ["V18", "V18"],
    ["V19", "V19"],
    ["V20", "V20"],
    ["V21", "V21"],
    ["V22", "V22"],
    ["V23", "V23"],
    ["V24", "V24"],
    ["V25", "V25"],
    ["V26", "V26"],
    ["V27", "V27"],
    ["V28", "V28"],
    ["V29", "V29"],
    ["V30", "V30"],
    ["V31", "V31"],
    ["V32", "V32"],
    ["V33", "V33"],
    ["V34", "V34"],
    ["V35", "V35"],
    ["V36", "V36"],
    ["V37", "V37"],
    ["V38", "V38"],
    ["V39", "V39"],
    ["V40", "V40"]
    ];
    
    var BLYNK_VIRTUALPIN_SELECT_new = [
        ["V0", "0"],
        ["V1", "1"],
        ["V2", "2"],
        ["V3", "3"],
        ["V4", "4"],
        ["V5", "5"],
        ["V6", "6"],
        ["V7", "7"],
        ["V8", "8"],
        ["V9", "9"],
        ["V10", "10"],
        ["V11", "11"],
        ["V12", "12"],
        ["V13", "13"],
        ["V14", "14"],
        ["V15", "15"],
        ["V16", "16"],
        ["V17", "17"],
        ["V18", "18"],
        ["V19", "19"],
        ["V20", "20"],
        ["V21", "21"],
        ["V22", "22"],
        ["V23", "23"],
        ["V24", "24"],
        ["V25", "25"],
        ["V26", "26"],
        ["V27", "27"],
        ["V28", "28"],
        ["V29", "29"],
        ["V30", "30"],
        ["V31", "31"],
        ["V32", "32"],
        ["V33", "33"],
        ["V34", "34"],
        ["V35", "35"],
        ["V36", "36"],
        ["V37", "37"],
        ["V38", "38"],
        ["V39", "39"],
        ["V40", "40"]
        ];

    //定时器选择
    var BLYNK_TIMER_SELECT = [
    ["1", "1"],
    ["2", "2"],
    ["3", "3"],
    ["4", "4"],
    ["5", "5"],
    ["6", "6"],
    ["7", "7"],
    ["8", "8"],
    ["9", "9"],
    ["10", "10"],
    ["11", "11"],
    ["12", "12"],
    ["13", "13"],
    ["14", "14"],
    ["15", "15"],
    ["16", "16"],
    ];

  Blockly.Blocks.Blynk_init= {
    init: function() {
    this.appendDummyInput()
        .appendField("Blynk服务器信息");
    this.appendValueInput("ADDR")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("服务器地址");
    this.appendValueInput("POST")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("端口");
    this.appendValueInput("KEY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Blynk授权码");
    this.appendValueInput("PR")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("打印连接信息");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("连接Blynk服务器");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Blynk_run= {
    init: function() {
    this.appendDummyInput()
        .appendField("物联网");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("运行");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("Blynk程序正常运行，需要在程序中持续循环运行此模块");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Blynk_connected= {
    init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("物联网");
    this.appendDummyInput()
        .appendField("连接状态");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("获取Blynk服务器连接状态");
    this.setHelpUrl("");
    }
  };

  //从app端获取数据
Blockly.Blocks.blynk_iot_get_data = {
    /**
   * Block for defining a procedure with no return value.
   * @this Blockly.Block
   */
   init: function () {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("物联网");
    this.appendDummyInput("")
    .appendField('监测引脚 #');
    this.appendDummyInput("")
    .appendField(new Blockly.FieldDropdown(BLYNK_VIRTUALPIN_SELECT), "Vpin");
    this.appendDummyInput()
    .appendField("", "PARAMS");
      this.setMutator(new Blockly.Mutator(["procedures_mutatorarg"]));//添加齿轮
      this.setTooltip();
      this.setStyle('blynk_blocks');
      this.arguments_ = [];//新增参数名称
      this.argumentstype_ = [];//新增参数类型
      this.setStatements_(true);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.statementConnection_ = null;
    },
  
    getVars: function () {
      return [this.getFieldValue("VAR")];
    },
  
    renameVar: function (oldName, newName) {
      if (Blockly.Names.equals(oldName, this.getFieldValue("VAR"))) {
        this.setTitleValue(newName, "VAR");
      }
    },
  
    /**
     * Add or remove the statement block from this function definition.
     * @param {boolean} hasStatements True if a statement block is needed.
     * @this Blockly.Block
     */
     setStatements_: function (hasStatements) {
      if (this.hasStatements_ === hasStatements) {
        return;
      }
      if (hasStatements) {
        this.appendStatementInput("STACK")
        .appendField(Blockly.Msg.CONTROLS_REPEAT_INPUT_DO);
        if (this.getInput("RETURN")) {
          this.moveInputBefore("STACK", "RETURN");
        }
      } else {
        this.removeInput("STACK", true);
      }
      this.hasStatements_ = hasStatements;
    },
    /**
     * Update the display of parameters for this procedure definition block.
     * Display a warning if there are duplicately named parameters.
     * @private
     * @this Blockly.Block
     */
     updateParams_: function () {
      // Check for duplicated arguments.
      var badArg = false;
      var hash = {};
      for (var i = 0; i < this.arguments_.length; i++) {
        if (hash["arg_" + this.arguments_[i].toLowerCase()]) {
          badArg = true;
          break;
        }
        hash["arg_" + this.arguments_[i].toLowerCase()] = true;
      }
      if (badArg) {
        this.setWarningText(Blockly.Msg.PROCEDURES_DEF_DUPLICATE_WARNING);
      } else {
        this.setWarningText(null);
      }
      // Merge the arguments into a human-readable list.
      var paramString = "";
      if (this.arguments_.length) {
        paramString = Blockly.Msg.PROCEDURES_BEFORE_PARAMS +
        " " + this.arguments_.join(", ");
      }
      // The params field is deterministic based on the mutation,
      // no need to fire a change event.
      Blockly.Events.disable();
      this.setFieldValue(paramString, "PARAMS");
      Blockly.Events.enable();
    },
    /**
     * Create XML to represent the argument inputs.
     * @param {=boolean} opt_paramIds If true include the IDs of the parameter
     *     quarks.  Used by Blockly.Procedures.mutateCallers for reconnection.
     * @return {!Element} XML storage element.
     * @this Blockly.Block
     */
     mutationToDom: function () {
      var container = document.createElement("mutation");
      for (var i = 0; i < this.arguments_.length; i++) {
        var parameter = document.createElement("arg");
        parameter.setAttribute("name", this.arguments_[i]);
        parameter.setAttribute("vartype", this.argumentstype_[i]);//新增
        container.appendChild(parameter);
      }
  
      // Save whether the statement input is visible.
      if (!this.hasStatements_) {
        container.setAttribute("statements", "false");
      }
      return container;
    },
    /**
    * Parse XML to restore the argument inputs.
    * @param {!Element} xmlElement XML storage element.
    * @this Blockly.Block
    */
    domToMutation: function (xmlElement) {
      this.arguments_ = [];
      this.argumentstype_ = [];//新增
      for (var i = 0, childNode; childNode = xmlElement.childNodes[i]; i++) {
        if (childNode.nodeName.toLowerCase() == "arg") {
          this.arguments_.push(childNode.getAttribute("name"));
          this.argumentstype_.push(childNode.getAttribute("vartype"));//新增
        }
      }
      this.updateParams_();
     // Blockly.Procedures.mutateCallers(this);
  
      // Show or hide the statement input.
      this.setStatements_(xmlElement.getAttribute("statements") !== "false");
    },
    /**
     * Populate the mutator"s dialog with this block"s components.
     * @param {!Blockly.Workspace} workspace Mutator"s workspace.
     * @return {!Blockly.Block} Root block in mutator.
     * @this Blockly.Block
     */
     decompose: function (workspace) {
      var containerBlock = workspace.newBlock("procedures_mutatorcontainer");
      containerBlock.initSvg();
  
      // Check/uncheck the allow statement box.
      if (this.getInput("RETURN")) {
        containerBlock.setFieldValue(this.hasStatements_ ? "TRUE" : "FALSE",
          "STATEMENTS");
      } else {
        containerBlock.getInput("STATEMENT_INPUT").setVisible(false);
      }
  
      // Parameter list.
      var connection = containerBlock.getInput("STACK").connection;
      for (var i = 0; i < this.arguments_.length; i++) {
        var paramBlock = workspace.newBlock("procedures_mutatorarg");
        paramBlock.initSvg();
        paramBlock.setFieldValue(this.arguments_[i], "NAME");
        //paramBlock.setFieldValue(this.argumentstype_[i], "TYPEVAR");//新增
        // Store the old location.
        paramBlock.oldLocation = i;
        connection.connect(paramBlock.previousConnection);
        connection = paramBlock.nextConnection;
      }
      // Initialize procedure"s callers with blank IDs.
     // Blockly.Procedures.mutateCallers(this);
     return containerBlock;
   },
    /**
     * Reconfigure this block based on the mutator dialog"s components.
     * @param {!Blockly.Block} containerBlock Root block in mutator.
     * @this Blockly.Block
     */
     compose: function (containerBlock) {
      // Parameter list.
      this.arguments_ = [];
      this.paramIds_ = [];
      this.argumentstype_ = [];//新增
      var paramBlock = containerBlock.getInputTargetBlock("STACK");
      while (paramBlock) {
        this.arguments_.push(paramBlock.getFieldValue("NAME"));
        this.argumentstype_.push(paramBlock.getFieldValue("TYPEVAR"));//新增
        this.paramIds_.push(paramBlock.id);
        paramBlock = paramBlock.nextConnection &&
        paramBlock.nextConnection.targetBlock();
      }
      this.updateParams_();
    //  Blockly.Procedures.mutateCallers(this);
  
      // Show/hide the statement input.
      var hasStatements = containerBlock.getFieldValue("STATEMENTS");
      if (hasStatements !== null) {
        hasStatements = hasStatements == "TRUE";
        if (this.hasStatements_ != hasStatements) {
          if (hasStatements) {
            this.setStatements_(true);
            // Restore the stack, if one was saved.
            Blockly.Mutator.reconnect(this.statementConnection_, this, "STACK");
            this.statementConnection_ = null;
          } else {
            // Save the stack, then disconnect it.
            var stackConnection = this.getInput("STACK").connection;
            this.statementConnection_ = stackConnection.targetConnection;
            if (this.statementConnection_) {
              var stackBlock = stackConnection.targetBlock();
              stackBlock.unplug();
              stackBlock.bumpNeighbours_();
            }
            this.setStatements_(false);
          }
        }
      }
    },
    /**
     * Dispose of any callers.
     * @this Blockly.Block
     */
     dispose: function () {
      var name = this.getFieldValue("NAME");
     // Blockly.Procedures.disposeCallers(name, this.workspace);
      // Call parent"s destructor.
      this.constructor.prototype.dispose.apply(this, arguments);
    },
    /**
     * Return the signature of this procedure definition.
     * @return {!Array} Tuple containing three elements:
     *     - the name of the defined procedure,
     *     - a list of all its arguments,
     *     - that it DOES NOT have a return value.
     * @this Blockly.Block
     */
    // getProcedureDef: function () {
    //   return ["ignoreProcedureIotGetData", this.arguments_, false];
    // },
    /**
     * Return all variables referenced by this block.
     * @return {!Array.<string>} List of variable names.
     * @this Blockly.Block
     */
     getVars: function () {
      return this.arguments_;
    },
    /**
     * Notification that a variable is renaming.
     * If the name matches one of this block"s variables, rename it.
     * @param {string} oldName Previous name of variable.
     * @param {string} newName Renamed variable.
     * @this Blockly.Block
     */
     renameVar: function (oldName, newName) {
      var change = false;
      for (var i = 0; i < this.arguments_.length; i++) {
        if (Blockly.Names.equals(oldName, this.arguments_[i])) {
          this.arguments_[i] = newName;
          change = true;
        }
      }
      if (change) {
        this.updateParams_();
        // Update the mutator"s variables if the mutator is open.
        if (this.mutator.isVisible()) {
          var blocks = this.mutator.workspace_.getAllBlocks();
          for (var i = 0, block; block = blocks[i]; i++) {
            if (block.type == "procedures_mutatorarg" &&
              Blockly.Names.equals(oldName, block.getFieldValue("NAME"))) {
              block.setFieldValue(newName, "NAME");
          }
        }
      }
    }
  },
    /**
     * Add custom menu options to this block"s context menu.
     * @param {!Array} options List of menu options to add to.
     * @this Blockly.Block
     */
     customContextMenu: function (options) {
      // Add option to create caller.
      var option = { enabled: true };
      var name = this.getFieldValue("NAME");
      option.text = Blockly.Msg.PROCEDURES_CREATE_DO.replace("%1", name);
      var xmlMutation = Blockly.utils.xml.createElement("mutation");
      xmlMutation.setAttribute("name", name);
      for (var i = 0; i < this.arguments_.length; i++) {
        var xmlArg = Blockly.utils.xml.createElement("arg");
        xmlArg.setAttribute("name", this.arguments_[i]);
        xmlArg.setAttribute("type", this.argumentstype_[i]);//新增
        xmlMutation.appendChild(xmlArg);
      }
      var xmlBlock = Blockly.utils.xml.createElement("block", null, xmlMutation);
      xmlBlock.setAttribute("type", this.callType_);
      option.callback = Blockly.ContextMenu.callbackFactory(this, xmlBlock);
      options.push(option);
  
      // Add options to create getters for each parameter.
      if (!this.isCollapsed()) {
        for (var i = 0; i < this.arguments_.length; i++) {
          var option = { enabled: true };
          var name = this.arguments_[i];
          option.text = Blockly.Msg.VARIABLES_SET_CREATE_GET.replace("%1", name);
          var xmlField = Blockly.utils.xml.createElement("field", null, name);
          xmlField.setAttribute("name", "VAR");
          //xmlField.setAttribute("type", "TYPEVAR");//新增
          var xmlBlock = Blockly.utils.xml.createElement("block", null, xmlField);
          xmlBlock.setAttribute("type", "variables_get");
          option.callback = Blockly.ContextMenu.callbackFactory(this, xmlBlock);
          options.push(option);
        }
      }
    },
    callType_: "procedures_callnoreturn"
  };

  //blynk定时器
  Blockly.Blocks.Blynk_iot_timer = {
    init: function () {
      this.appendValueInput("TIME")
      .setCheck(Number)
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField('Blynk定时器')
      .appendField(new Blockly.FieldDropdown(BLYNK_TIMER_SELECT), "timerNo");
      this.appendDummyInput("")
      .appendField('毫秒');
      this.appendStatementInput("DO")
      .appendField('执行');
      this.setStyle('blynk_blocks');
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
    }
  };

  //发送数据到app
  Blockly.Blocks.blynk_iot_push_data = {
    init: function () {
      this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("物联网");
      this.appendDummyInput("")
      .appendField('发送数据到App');
      this.appendDummyInput("")
      .appendField(new Blockly.FieldDropdown(BLYNK_VIRTUALPIN_SELECT_new), "Vpin");
      this.appendValueInput("data")
      .appendField('数据');
      this.setStyle('blynk_blocks');
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setInputsInline(true);
      this.setTooltip(" ");
      this.setHelpUrl();
    }
  };

  Blockly.Blocks.Blynk_time_run= {
    init: function() {
    this.appendDummyInput()
        .appendField("物联网Blynk定时器运行")
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("Blynk定时器正常运行，需要在程序中持续循环运行此模块");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Blynk_led= {
    init: function() {
    this.appendDummyInput()
        .appendField("物联网");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("LED组件 虚拟引脚")
        .appendField(new Blockly.FieldDropdown(BLYNK_VIRTUALPIN_SELECT_new), "Vpin");
    this.appendValueInput("COLOR")
        .setCheck(null)
        .appendField("颜色");
    this.appendValueInput("PT")
        .setCheck(null)
        .appendField("亮度");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("设置LED组件状态");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.RGB_color_seclet = {
    init: function () {
      this.setColour(135);
      this.appendDummyInput("")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField(new Blockly.FieldColour("ff0000"), "COLOR");
      this.setInputsInline(true);
      this.setOutput(true, Number);
      this.setTooltip(Blockly.OLED_DRAW_PIXE_TOOLTIP);
    }
  };

  Blockly.Blocks.Blynk_email= {
    init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Blynk发送邮件");
    this.appendValueInput("TET")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("邮件主题");
    this.appendValueInput("BODY")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("邮件内容");
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("Blynk发送邮件");
    this.setHelpUrl("");
    }
  };


  Blockly.Blocks.Blynk_set_color= {
    init: function() {
    this.appendDummyInput()
        .appendField("物联网");
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput()
        .appendField(" 虚拟引脚")
        .appendField(new Blockly.FieldDropdown(BLYNK_VIRTUALPIN_SELECT_new), "Vpin");
    this.appendValueInput("COLOR")
        .setCheck(null)
        .appendField("组件颜色");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('blynk_blocks');
    this.setTooltip("设置组件颜色");
    this.setHelpUrl("");
    }
  };