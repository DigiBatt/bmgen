Blockly.BTS600['controls_if'] = function (block) {
  // If/elseif/else condition.
  let n = 0;
  let code = '';
  do {
    const conditionCode =
      JavaScript.valueToCode(block, 'IF' + n, JavaScript.ORDER_NONE) ||
      'false';
    let branchCode = JavaScript.statementToCode(block, 'DO' + n);
    if (JavaScript.STATEMENT_SUFFIX) {
      branchCode = JavaScript.prefixLines(
        JavaScript.injectId(JavaScript.STATEMENT_SUFFIX, block),
        JavaScript.INDENT) +
        branchCode;
    }
    code += (n > 0 ? ' else ' : '') + 'if (' + conditionCode + ') {\n' +
      branchCode + '}';
    n++;
  } while (block.getInput('IF' + n));

  if (block.getInput('ELSE') || JavaScript.STATEMENT_SUFFIX) {
    let branchCode = JavaScript.statementToCode(block, 'ELSE');
    if (JavaScript.STATEMENT_SUFFIX) {
      branchCode = JavaScript.prefixLines(
        JavaScript.injectId(JavaScript.STATEMENT_SUFFIX, block),
        JavaScript.INDENT) +
        branchCode;
    }
    code += ' else {\n' + branchCode + '}';
  }
  return code + '\n';
};

Blockly.BTS600['controls_ifelse'] = Blockly.BTS600['controls_if'];