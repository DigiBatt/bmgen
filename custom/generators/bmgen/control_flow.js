goog.module("BMGen3000.Generator.ControlFlow");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['function_cycle'] = function (block) {
    const name = 'cycle';
    const count = block.getFieldValue('COUNT');
    var body = Generator.statementToCode(block, 'ARGS').replace(/\n/g, '\n\t');
    return `${name}(${count}) {\n\t${body}\n}`;
}

Generator['while'] = function (block) {
    const condition = Generator.valueToCode(block, 'CONDITION');
    var body = Generator.statementToCode(block, 'PROGRAM').replace(/\n/g, '\n\t');
    return `while (${condition}) {\n\t${body}\n}`;
}

Generator['for'] = function (block) {
    const init_statement = Generator.statementToCode(block, 'INIT_STATEMENT').replace(/;$/, '');
    const condition = Generator.valueToCode(block, 'CONDITION');
    const loop_statement = Generator.statementToCode(block, 'LOOP_STATEMENT').replace(/;$/, '');
    var body = Generator.statementToCode(block, 'PROGRAM').replace(/\n/g, '\n\t');
    return `for (${init_statement}; ${condition}; ${loop_statement}) {\n\t${body}\n}`;
}

Generator['if_else'] = function (block) {
    let code = `if (${Generator.valueToCode(block, 'IF0')}) {\n\t${Generator.statementToCode(block, 'DO0').replace(/\n/g, '\n\t')}\n}`;
    for (let i = 1; i <= block.elseifCount_; i++) {
        code += ` elseif (${Generator.valueToCode(block, `IF${i}`)}) {\n\t${Generator.statementToCode(block, `DO${i}`).replace(/\n/g, '\n\t')}\n}`;
    }
    if (block.elseCount_) {
        code += ` else {\n\t${Generator.statementToCode(block, `ELSE`).replace(/\n/g, '\n\t')}\n}`;
    }
    return code;
}