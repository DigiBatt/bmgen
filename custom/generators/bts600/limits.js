Blockly.BTS600['limit'] = function (block) {
    const limit = Blockly.BTS600.valueToCode(block, 'EXPRESSION');
    return limit;
}

Blockly.BTS600['limit_action'] = function (block) {
    const limit = Blockly.BTS600.valueToCode(block, 'EXPRESSION');
    const action = Blockly.BTS600.statementToCode(block, 'ACTION');
    limit.action = action.action;
    return limit;
}

Blockly.BTS600['compare'] = function (block) {
    const OPERATORS =
        { 'GT': '>', 'LT': '<', 'GTE': '>=', 'LTE': '<=' };
    const operator = OPERATORS[block.getFieldValue('OPERATOR')];
    const factor = Blockly.BTS600.valueToCode(block, 'FACTOR');
    const channel = Blockly.BTS600.valueToCode(block, 'CHANNEL');
    var code = new BTSLine();
    code.limit = `${operator} ${factor} ${channel}`;
    return code;
}

Blockly.BTS600['time'] = function (block) {
    const UNITS =
        { 'SECONDS': 'sec', 'MINUTES': 'min', 'HOURS': 'h' };
    const unit = UNITS[block.getFieldValue('UNIT')];
    const value = block.getFieldValue('VALUE');
    var code = new BTSLine();
    code.limit = `> ${value} ${unit}`;
    return code;
}