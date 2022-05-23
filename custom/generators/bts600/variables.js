Blockly.BTS600['variable'] = function (block) {
    const variable = block.getFieldValue('VARIABLE');
    return new BTSVariable(variable);
};

Blockly.BTS600['assignment'] = function (block) {
    const variable = Blockly.BTS600.valueToCode(block, 'LHS');
    const value = new BTSNumber(block.getFieldValue('RHS'));
    return new BTSAssignment(variable, value);
};