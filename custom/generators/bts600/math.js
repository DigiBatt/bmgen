Blockly.BTS600['factor'] = function (block) {
    const factor = Blockly.BTS600.valueToCode(block, 'FACTOR');
    const value = Blockly.BTS600.valueToCode(block, 'VALUE');
    return `${factor} ${value}`;
};

Blockly.BTS600['math_number'] = function (block) {
    const number = block.getFieldValue('NUM');
    return `${number}`;
};