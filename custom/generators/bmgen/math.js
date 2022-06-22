Blockly.BMGen['number'] = function (block) {
    const number = block.getFieldValue('NUMBER');
    return `${number}`;
}