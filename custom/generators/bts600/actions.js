Blockly.BTS600['goto'] = function (block) {
    const label = block.getFieldValue('label');
    const code = '\t\t\t\t\tGOTO ' + label + '\t\n';
    return code;
}

Blockly.BTS600['label'] = function (block) {
    const label = block.getFieldValue('label');
    const code = '\t' + label + '\t\t\t\t\t\n';
    return code;
};