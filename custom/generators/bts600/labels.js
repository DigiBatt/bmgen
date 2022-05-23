Blockly.BTS600['label'] = function (block) {
    var code = new BTSLine();
    const label = block.getFieldValue('LABEL');
    code.label = label
    return code;
};

Blockly.BTS600['comment'] = function (block) {
    const comment = block.getFieldValue('COMMENT');
    return new BTSComment(comment);
};
