Blockly.BTS600['channel'] = function (block) {
    const channel = block.getFieldValue('CHANNEL');
    return new BTSVariable(channel);
};