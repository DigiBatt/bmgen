Blockly.BTS600['goto'] = function (block) {
    var code = new BTSLine();
    const label = block.getFieldValue('LABEL');
    code.action = `GOTO ${label}`
    return code;
}

Blockly.BTS600['err'] = function (block) {
    var code = new BTSLine();
    const errnum = block.getFieldValue('ERRNUM');
    code.action = `ERR ${errnum}`
    return code;
};