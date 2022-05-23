Blockly.BTS600['factor'] = function (block) {
    const lhs = Blockly.BTS600.valueToCode(block, 'FACTOR');
    const rhs = Blockly.BTS600.valueToCode(block, 'VALUE');
    return new BTSMultiplication(lhs, rhs);
};

Blockly.BTS600['math_number'] = function (block) {
    const number = block.getFieldValue('NUM');
    return new BTSNumber(number);
};