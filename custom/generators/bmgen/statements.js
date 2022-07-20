goog.module("BMGen3000.Generator.Statements");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['assignment'] = function (block) {
    const lhs = Generator.valueToCode(block, 'LHS');
    const rhs = Generator.valueToCode(block, 'RHS');
    return `${lhs} = ${rhs};`;
}

Generator['setvalue'] = function (block) {
    const channel = Generator.valueToCode(block, 'CHANNEL');
    const value = Generator.valueToCode(block, 'VALUE');
    return `${value} ${channel}`;
}

Generator['empty_function'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}();`;
}

Generator['function'] = function (block) {
    const name = block.getFieldValue('NAME');
    var args = Generator.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Generator['function_charge'] = function (block) {
    const name = 'charge';
    var args = Generator.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Generator['function_discharge'] = function (block) {
    const name = 'discharge';
    var args = Generator.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}

Generator['function_pause'] = function (block) {
    const name = 'pause';
    var args = Generator.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `${name}(${args});`;
}