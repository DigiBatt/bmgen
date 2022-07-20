goog.module("BMGen3000.Generator.Arrays");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['array_init'] = function (block) {
    let values = [];
    for (let i = 0; i < block.itemCount_; i++) {
        values.push(Generator.valueToCode(block, `ADD${i}`));
    }
    return '[' + values.join(', ') + ']';
}

Generator['array_access'] = function (block) {
    return `${Generator.valueToCode(block, 'ARRAY')}[${Generator.valueToCode(block, 'INDEX')}]`;
}