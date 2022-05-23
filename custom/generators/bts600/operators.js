Blockly.BTS600['set'] = function (block) {
  var value = Blockly.BTS600.statementToCode(block, 'VALUE');
  var limit = Blockly.BTS600.statementToCode(block, 'LIMIT');
  var registration = Blockly.BTS600.statementToCode(block, 'REGISTRATION');
  return new BTSStatement('SET', value, limit, registration);
};

Blockly.BTS600['beg'] = function (block) {
  return new BTSStatement('BEG', [], [], []);
};

Blockly.BTS600['cyc'] = function (block) {
  const value = block.getFieldValue('COUNT');
  var cyclecount = new BTSCycleCount(new BTSNumber(value));
  return new BTSStatement('CYC', [cyclecount], [], []);
};

Blockly.BTS600['cha'] = function (block) {
  const values = [Blockly.BTS600.valueToCode(block, 'VALUE')];
  const limits = Blockly.BTS600.statementToCode(block, 'LIMIT');
  return new BTSStatement('CHA', values, limits, []);
};

Blockly.BTS600['dch'] = function (block) {
  const values = [Blockly.BTS600.valueToCode(block, 'VALUE')];
  const limits = Blockly.BTS600.statementToCode(block, 'LIMIT');
  return new BTSStatement('DCH', values, limits, []);
};

Blockly.BTS600['sto'] = function (block) {
  return new BTSStatement('STO', [], [], []);
};

Blockly.BTS600['pau'] = function (block) {
  var limits = Blockly.BTS600.statementToCode(block, 'LIMIT');
  console.log(limits);
  return new BTSStatement('PAU', [], limits, []);
};