goog.module("BMGen3000.Generator.Channels");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['channel'] = function (block) {
    const name = block.getFieldValue('NAME');
    return `${name}`;
}