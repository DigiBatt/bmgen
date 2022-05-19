Blockly.BTS600['set'] = function (block) {
  var value = Blockly.BTS600.statementToCode(block, 'VALUE');
  if (value instanceof Array) {
    const combined = value.map(line => line.value).join('\n');
    value = new BTSLine();
    value.value = combined;
    value.operator = 'SET';
  }
  else if (value instanceof BTSLine) {
    value.operator = 'SET';
  }

  var limit = Blockly.BTS600.statementToCode(block, 'LIMIT');
  if (limit instanceof Array) {
    const combined = limit.map(line => line.limit).join('\n');
    const combined_action = limit.map(line => line.action).join('\n');
    limit = new BTSLine();
    limit.limit = combined;
    limit.action = combined_action;
    limit.operator = 'SET';
  }
  else if (limit instanceof BTSLine) {
    limit.operator = 'SET';
  }

  var registration = Blockly.BTS600.statementToCode(block, 'REGISTRATION');
  if (registration instanceof Array) {
    const combined = registration.map(line => line.registration).join('\n');
    registration = new BTSLine();
    registration.registration = combined;
    registration.operator = 'SET';
  }
  else if (registration instanceof BTSLine) {
    registration.operator = 'SET';
  }

  return BTSLine.concat(BTSLine.concat(value, limit), registration);
};

Blockly.BTS600['beg'] = function (block) {
  var code = new BTSLine();
  code.operator = 'BEG';
  const cyclename = block.getFieldValue('NAME');
  code.value = cyclename;
  return code;
};

Blockly.BTS600['cyc'] = function (block) {
  var code = new BTSLine();
  code.operator = 'CYC';
  const cyclecount = block.getFieldValue('COUNT');
  code.value = `${cyclecount} *`;
  return code;
};

Blockly.BTS600['cha'] = function (block) {
  const value = Blockly.BTS600.valueToCode(block, 'VALUE');
  var line = Blockly.BTS600.statementToCode(block, 'LIMIT');
  if (!line) {
    line = new BTSLine();
  }
  line.operator = 'CHA';
  line.value = value;
  return line;
};

Blockly.BTS600['dch'] = function (block) {
  const value = Blockly.BTS600.valueToCode(block, 'VALUE');
  var line = Blockly.BTS600.statementToCode(block, 'LIMIT');
  if (!line) {
    line = new BTSLine();
  }
  line.operator = 'DCH';
  line.value = value;
  return line;
};

Blockly.BTS600['sto'] = function (block) {
  var line = new BTSLine();
  line.operator = 'STO';
  return line;
};

Blockly.BTS600['pau'] = function (block) {
  var line = Blockly.BTS600.statementToCode(block, 'LIMIT');
  if (!line) {
    line = new BTSLine();
  }
  line.operator = 'PAU';
  return line;
};