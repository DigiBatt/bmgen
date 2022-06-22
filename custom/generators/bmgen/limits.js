Blockly.BMGen['action_error'] = function (block) {
    const errnum = block.getFieldValue('ERRNUM');
    return `error(${errnum})`;
}

Blockly.BMGen['action_goto'] = function (block) {
    const label = block.getFieldValue('LABEL');
    return `goto(${label})`;
}

Blockly.BMGen['time'] = function (block) {
    const value = block.getFieldValue('VALUE');
    const unit = block.getFieldValue('UNIT');
    return `${value} ${unit}`;
}

Blockly.BMGen['comparison'] = function (block) {
    const lhs = Blockly.BMGen.valueToCode(block, 'LHS');
    const rhs = Blockly.BMGen.valueToCode(block, 'RHS');
    const operator = block.getFieldValue('OPERATOR');
    return `${lhs} ${operator} ${rhs}`;
}

Blockly.BMGen['limit'] = function (block) {
    const condition = Blockly.BMGen.valueToCode(block, 'CONDITION');
    return `limit(${condition});`;
}

Blockly.BMGen['limit_action'] = function (block) {
    const condition = Blockly.BMGen.valueToCode(block, 'CONDITION');
    const action = Blockly.BMGen.valueToCode(block, 'ACTION');
    return `limit(${condition}, ${action});`;
}