goog.module("BMGen3000.Generator.Limits");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['action_error'] = function (block) {
    const errnum = block.getFieldValue('ERRNUM');
    return `error(${errnum})`;
}

Generator['action_goto'] = function (block) {
    const label = block.getFieldValue('LABEL');
    return `goto(${label})`;
}

Generator['time'] = function (block) {
    const value = block.getFieldValue('VALUE');
    const unit = block.getFieldValue('UNIT');
    return `${value} ${unit}`;
}

Generator['comparison'] = function (block) {
    const lhs = Generator.valueToCode(block, 'LHS');
    const rhs = Generator.valueToCode(block, 'RHS');
    const operator = block.getFieldValue('OPERATOR');
    return `${lhs} ${operator} ${rhs}`;
}

Generator['limit'] = function (block) {
    const condition = Generator.valueToCode(block, 'CONDITION');
    return `limit(${condition});`;
}

Generator['limit_action'] = function (block) {
    const condition = Generator.valueToCode(block, 'CONDITION');
    const action = Generator.valueToCode(block, 'ACTION');
    return `limit(${condition}, ${action});`;
}

Generator['limit_and'] = function (block) {
    const lhs = Generator.valueToCode(block, 'LHS');
    const rhs = Generator.valueToCode(block, 'RHS');
    return `${lhs} & ${rhs}`;
}