Blockly.BTS600['label'] = function (block) {
    var code = new BTSLine();
    const label = block.getFieldValue('LABEL');
    code.label = label
    return code;
};

Blockly.BTS600['comment'] = function (block) {
    var code = new BTSLine();
    const comment = block.getFieldValue('COMMENT');
    code.label = '! ' + comment;
    return code;
};
