Blockly.BTS600['variable'] = function (block) {
    const variable = block.getFieldValue('VARIABLE');
    return variable;
};

Blockly.BTS600['assignment'] = function (block) {
    const variable = Blockly.BTS600.valueToCode(block, 'LHS');
    const value = block.getFieldValue('RHS');
    let code = new BTSLine();
    code.value = `${variable} = ${value}`;
    return code;
};