goog.module("BMGen3000.Generator.Math");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['math'] = function (block) {
    const lhs = Generator.valueToCode(block, 'LHS');
    const rhs = Generator.valueToCode(block, 'RHS');
    const operator = block.getFieldValue('OPERATOR');
    return `${lhs} ${operator} ${rhs};`;
}
