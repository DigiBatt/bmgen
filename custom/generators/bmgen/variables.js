goog.module("BMGen3000.Generator.Variables");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['variable'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}`;
}