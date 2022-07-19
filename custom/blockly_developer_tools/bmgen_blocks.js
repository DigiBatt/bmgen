Blockly.Blocks['limit'] = {
  init: function () {
    this.appendValueInput("CONDITION")
      .setCheck("LimitCondition")
      .appendField("limit");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(90);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['limit_action'] = {
  init: function () {
    this.appendValueInput("CONDITION")
      .setCheck("LimitCondition")
      .appendField("limit");
    this.appendValueInput("ACTION")
      .setCheck("Action")
      .appendField("action");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(90);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['action_error'] = {
  init: function () {
    this.appendDummyInput()
      .appendField("error")
      .appendField(new Blockly.FieldNumber(0, 0, Infinity, 1), "ERRNUM");
    this.setInputsInline(true);
    this.setOutput(true, "Action");
    this.setColour(0);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['action_goto'] = {
  init: function () {
    this.appendDummyInput()
      .appendField("goto")
      .appendField(new Blockly.FieldTextInput("label"), "LABEL");
    this.setInputsInline(true);
    this.setOutput(true, "Action");
    this.setColour(0);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['assignment'] = {
  init: function () {
    this.appendValueInput("LHS")
      .setCheck(["Variable", "Channel"]);
    this.appendValueInput("RHS")
      .setCheck(["Number", "Variable", "Numvalue", "Channel"])
      .appendField("=");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(60);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['function'] = {
  init: function () {
    this.appendStatementInput("ARGS")
      .setCheck(null)
      .appendField(new Blockly.FieldTextInput("function"), "NAME");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['function_cycle'] = {
  init: function () {
    this.appendDummyInput()
      .appendField("cycle")
      .appendField(new Blockly.FieldNumber(5, 0, Infinity, 1), "COUNT")
      .appendField("*");
    this.appendStatementInput("ARGS")
      .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['while'] = {
  init: function () {
    this.appendValueInput("CONDITION")
      .setCheck("LimitCondition")
      .appendField("while (");
    this.appendDummyInput()
      .appendField(")");
    this.appendStatementInput("PROGRAM")
      .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['for'] = {
  init: function () {
    this.appendStatementInput("INIT_STATEMENT")
      .setCheck(null)
      .appendField("for (");
    this.appendDummyInput()
      .appendField(";");
    this.appendValueInput("CONDITION")
      .setCheck("LimitCondition");
    this.appendDummyInput()
      .appendField(";");
    this.appendStatementInput("LOOP_STATEMENT")
      .setCheck(null)
    this.appendDummyInput()
      .appendField(")");
    this.appendStatementInput("PROGRAM")
      .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['function_pause'] = {
  init: function () {
    this.appendStatementInput("ARGS")
      .setCheck(null)
      .appendField("pause");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['comparison'] = {
  init: function () {
    this.appendValueInput("LHS")
      .setCheck(["Channel", "Variable"]);
    this.appendValueInput("RHS")
      .setCheck(["Number", "Variable", "Channel"])
      .appendField(new Blockly.FieldDropdown([["<", "<"], [">", ">"], ["<=", "<="], [">=", ">="], ["=", "="]]), "OPERATOR");
    this.setInputsInline(true);
    this.setOutput(true, "LimitCondition");
    this.setColour(90);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['time'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldNumber(0, 0), "VALUE")
      .appendField(new Blockly.FieldDropdown([["sec", "sec"], ["min", "min"], ["h", "h"]]), "UNIT");
    this.setInputsInline(true);
    this.setOutput(true, "LimitCondition");
    this.setColour(90);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['function_discharge'] = {
  init: function () {
    this.appendStatementInput("ARGS")
      .setCheck(null)
      .appendField("discharge");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['function_charge'] = {
  init: function () {
    this.appendStatementInput("ARGS")
      .setCheck(null)
      .appendField("charge");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['variable'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldLabelSerializable(""), "NAME");
    this.setOutput(true, "Variable");
    this.setColour(290);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['channel'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldLabelSerializable(""), "NAME");
    this.setOutput(true, "Channel");
    this.setColour(260);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['number'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldNumber(0), "NUMBER");
    this.setOutput(true, "Number");
    this.setColour(160);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['comment'] = {
  init: function () {
    this.appendDummyInput()
      .appendField("comment")
      .appendField(new Blockly.FieldTextInput("text"), "TEXT");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(165);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['label'] = {
  init: function () {
    this.appendDummyInput()
      .appendField("label")
      .appendField(new Blockly.FieldTextInput("text"), "LABEL");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(165);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['registration'] = {
  init: function () {
    this.appendStatementInput("ARGS")
      .setCheck(null)
      .appendField("registration");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(345);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['regname'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldLabelSerializable(""), "NAME");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['setvalue'] = {
  init: function () {
    this.appendValueInput("VALUE")
      .setCheck(["Number", "Variable", "Numvalue"]);
    this.appendValueInput("CHANNEL")
      .setCheck("Channel");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(60);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['empty_function'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(new Blockly.FieldTextInput("function"), "NAME");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['math'] = {
  init: function () {
    this.appendValueInput("LHS")
      .setCheck(["Variable", "Channel"]);
    this.appendValueInput("RHS")
      .setCheck(["Number", "Variable", "Numvalue", "Channel"])
      .appendField(new Blockly.FieldDropdown([["+=", "+="], ["-=", "-="]]), "OPERATOR");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(60);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};

Blockly.Blocks['limit_and'] = {
  init: function () {
    this.appendValueInput("LHS")
      .setCheck("LimitCondition");
    this.appendValueInput("RHS")
      .setCheck("LimitCondition")
      .appendField("&");
    this.setInputsInline(true);
    this.setOutput(true, "LimitCondition");
    this.setColour(90);
    this.setTooltip("");
    this.setHelpUrl("");
  }
};