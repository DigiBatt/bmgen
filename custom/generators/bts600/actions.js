Blockly.BTS600['goto'] = function (block) {
    return new BTSGoto(label);
}

Blockly.BTS600['err'] = function (block) {
    const errnum = block.getFieldValue('ERRNUM');
    return new BTSError(errnum);
};