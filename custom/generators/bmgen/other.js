Blockly.BMGen['number'] = function (block) {
    const number = block.getFieldValue('NUMBER');
    return `${number}`;
}

Blockly.BMGen['comment'] = function (block) {
    const text = block.getFieldValue('TEXT');
    return `// ${text}`;
}

Blockly.BMGen['label'] = function (block) {
    const label = block.getFieldValue('LABEL');
    return `\n:${label}`;
}