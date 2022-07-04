goog.module("BMGen3000.Generator.Registrations");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['registration'] = function (block) {
    var args = Generator.statementToCode(block, 'ARGS').replace(/\n/g, ', ').replace(/;/g, '');
    return `registration(${args});`;
}

Generator['regname'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}`;
}