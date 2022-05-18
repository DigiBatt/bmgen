'use strict';

goog.module('Blockly.BTS600.jumps');

const BTS600 = goog.require('Blockly.BTS600');

BTS600['goto'] = function (block) {
    const label = block.getFieldValue('label');
    const code = 'goto ' + label + ';\n';
    return code;
}

BTS600['label'] = function (block) {
    const label = block.getFieldValue('label');
    const code = ':' + label + ';\n';
    return code;
};