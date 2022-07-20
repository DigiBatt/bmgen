const xmlUtils = Blockly.utils.xml;
const Align = Blockly.Input.Align;
const Msg = Blockly.Msg;
const Mutator = Blockly.Mutator;

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
      .setCheck(["Number", "Variable", "Numvalue", "Channel", "Array"])
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

Blockly.Blocks['array_init'] = {
  /**
   * Block for creating a list with any number of elements of any type.
   * @this {Block}
   */
  init: function () {
    this.setStyle('list_blocks');
    this.itemCount_ = 3;
    this.updateShape_();
    this.setOutput(true, 'Array');
    this.setMutator(new Mutator(['lists_create_with_item']));
    this.setTooltip(Msg['LISTS_CREATE_WITH_TOOLTIP']);
  },
  /**
   * Create XML to represent list inputs.
   * Backwards compatible serialization implementation.
   * @return {!Element} XML storage element.
   * @this {Block}
   */
  mutationToDom: function () {
    const container = xmlUtils.createElement('mutation');
    container.setAttribute('items', this.itemCount_);
    return container;
  },
  /**
   * Parse XML to restore the list inputs.
   * Backwards compatible serialization implementation.
   * @param {!Element} xmlElement XML storage element.
   * @this {Block}
   */
  domToMutation: function (xmlElement) {
    this.itemCount_ = parseInt(xmlElement.getAttribute('items'), 10);
    this.updateShape_();
  },
  /**
   * Returns the state of this block as a JSON serializable object.
   * @return {{itemCount: number}} The state of this block, ie the item count.
   */
  saveExtraState: function () {
    return {
      'itemCount': this.itemCount_,
    };
  },
  /**
   * Applies the given state to this block.
   * @param {*} state The state to apply to this block, ie the item count.
   */
  loadExtraState: function (state) {
    this.itemCount_ = state['itemCount'];
    this.updateShape_();
  },
  /**
   * Populate the mutator's dialog with this block's components.
   * @param {!Workspace} workspace Mutator's workspace.
   * @return {!Block} Root block in mutator.
   * @this {Block}
   */
  decompose: function (workspace) {
    const containerBlock = workspace.newBlock('lists_create_with_container');
    containerBlock.initSvg();
    let connection = containerBlock.getInput('STACK').connection;
    for (let i = 0; i < this.itemCount_; i++) {
      const itemBlock = workspace.newBlock('lists_create_with_item');
      itemBlock.initSvg();
      connection.connect(itemBlock.previousConnection);
      connection = itemBlock.nextConnection;
    }
    return containerBlock;
  },
  /**
   * Reconfigure this block based on the mutator dialog's components.
   * @param {!Block} containerBlock Root block in mutator.
   * @this {Block}
   */
  compose: function (containerBlock) {
    let itemBlock = containerBlock.getInputTargetBlock('STACK');
    // Count number of inputs.
    const connections = [];
    while (itemBlock && !itemBlock.isInsertionMarker()) {
      connections.push(itemBlock.valueConnection_);
      itemBlock =
        itemBlock.nextConnection && itemBlock.nextConnection.targetBlock();
    }
    // Disconnect any children that don't belong.
    for (let i = 0; i < this.itemCount_; i++) {
      const connection = this.getInput('ADD' + i).connection.targetConnection;
      if (connection && connections.indexOf(connection) === -1) {
        connection.disconnect();
      }
    }
    this.itemCount_ = connections.length;
    this.updateShape_();
    // Reconnect any child blocks.
    for (let i = 0; i < this.itemCount_; i++) {
      Mutator.reconnect(connections[i], this, 'ADD' + i);
    }
  },
  /**
   * Store pointers to any connected child blocks.
   * @param {!Block} containerBlock Root block in mutator.
   * @this {Block}
   */
  saveConnections: function (containerBlock) {
    let itemBlock = containerBlock.getInputTargetBlock('STACK');
    let i = 0;
    while (itemBlock) {
      const input = this.getInput('ADD' + i);
      itemBlock.valueConnection_ = input && input.connection.targetConnection;
      itemBlock =
        itemBlock.nextConnection && itemBlock.nextConnection.targetBlock();
      i++;
    }
  },
  /**
   * Modify this block to have the correct number of inputs.
   * @private
   * @this {Block}
   */
  updateShape_: function () {
    if (this.itemCount_ && this.getInput('EMPTY')) {
      this.removeInput('EMPTY');
    } else if (!this.itemCount_ && !this.getInput('EMPTY')) {
      this.appendDummyInput('EMPTY').appendField(
        'new array');
    }
    // Add new inputs.
    for (let i = 0; i < this.itemCount_; i++) {
      if (!this.getInput('ADD' + i)) {
        const input = this.appendValueInput('ADD' + i).setAlign(Align.RIGHT).setCheck(["Number"]);
        if (i === 0) {
          input.appendField('new array');
        }
      }
    }
    // Remove deleted inputs.
    for (let i = this.itemCount_; this.getInput('ADD' + i); i++) {
      this.removeInput('ADD' + i);
    }
  },
};

Blockly.Blocks['array_access'] = {
  init: function () {
    this.appendValueInput("ARRAY")
      .setCheck(["Variable"]);
    this.appendValueInput("INDEX")
      .setCheck(["Number", "Variable"])
      .appendField("[");
    this.appendDummyInput()
      .appendField("]");
    this.setInputsInline(true);
    this.setColour(60);
    this.setTooltip("");
    this.setHelpUrl("");
    this.setOutput(true, "Variable");
  }
};