Blockly.BMGen['variable'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}`;
}