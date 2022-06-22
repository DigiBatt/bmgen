Blockly.BMGen['assignment'] = function (block) {
    const lhs = Blockly.BMGen.valueToCode(block, 'LHS');
    const rhs = Blockly.BMGen.valueToCode(block, 'RHS');
    return `${lhs} = ${rhs};`;
}

Blockly.BMGen['function'] = function (block) {
    const name = block.getFieldValue('NAME');
    var args = Blockly.BMGen.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Blockly.BMGen['function_charge'] = function (block) {
    const name = 'charge';
    var args = Blockly.BMGen.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Blockly.BMGen['function_discharge'] = function (block) {
    const name = 'discharge';
    var args = Blockly.BMGen.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Blockly.BMGen['function_pause'] = function (block) {
    const name = 'pause';
    var args = Blockly.BMGen.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Blockly.BMGen['function_cycle'] = function (block) {
    const name = 'cycle';
    const count = block.getFieldValue('COUNT');
    var body = Blockly.BMGen.statementToCode(block, 'ARGS').replace(/\n/g, '\n\t');
    return `${name}(${count}) {\n\t${body}\n}`;
}
