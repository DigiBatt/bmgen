Blockly.BMGen['channel'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}`;
}