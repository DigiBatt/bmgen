goog.module("BMGen3000.Generator.Other");
let { Generator } = goog.require("BMGen3000.Generator");

Generator['number'] = function (block) {
    const number = block.getFieldValue('NUMBER');
    return `${number}`;
}

Generator['comment'] = function (block) {
    const text = block.getFieldValue('TEXT');
    return `// ${text}`;
}

Generator['label'] = function (block) {
    const label = block.getFieldValue('LABEL');
    return `\n:${label}`;
}