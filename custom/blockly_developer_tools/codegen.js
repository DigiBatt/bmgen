Blockly.JavaScript['goto'] = function (block) {
  var label = block.getFieldValue('label');
  var code = 'goto ' + label + ';\n';
  return code;
};

Blockly.JavaScript['label'] = function (block) {
  var label = block.getFieldValue('label');
  var code = ':' + label + ';\n';
  return code;
};