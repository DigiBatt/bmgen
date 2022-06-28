goog.module("BMGen3000.BMGenToBTS");

let bmgen_bts_converter = {};

const bmgen_function_map = {
    'pause': 'PAU',
    'charge': 'CHA',
    'discharge': 'DCH'
}

bmgen_bts_converter['assignment'] = function (json) {
    return `SET VALUE ${obj_to_bts(json.lhs)} = ${obj_to_bts(json.rhs)};`;
}

bmgen_bts_converter['function'] = function (json) {
    var name = json.name;
    if (name in bmgen_function_map) {
        name = bmgen_function_map[name];
    }
    return name + ' ' + json.args.map(x => obj_to_bts(x)).join(' ') + ';';
}

bmgen_bts_converter['limit_global'] = function (json) {
    var text = 'SET LIMIT ' + obj_to_bts(json.condition);
    if (json.action) {
        text += ' ' + obj_to_bts(json.action);
    }
    text += ';';
    return text;
}

bmgen_bts_converter['limit'] = function (json) {
    var text = 'LIMIT ' + obj_to_bts(json.condition);
    if (json.action) {
        text += ' ' + obj_to_bts(json.action);
    }
    return text;
}

bmgen_bts_converter['comparison'] = function (json) {
    return `${json.operator} ${obj_to_bts(json.rhs)} ${obj_to_bts(json.lhs)}`;
}

bmgen_bts_converter['error'] = function (json) {
    return `ACTION ERR ${json.errnum}`;
}

bmgen_bts_converter['setvalue'] = function (json) {
    return `VALUE ${obj_to_bts(json.rhs)} ${obj_to_bts(json.lhs)}`;
}

bmgen_bts_converter['time'] = function (json) {
    return `> ${obj_to_bts(json.value)} ${json.unit}`;
}

bmgen_bts_converter['cycle'] = function (json) {
    return 'BEG;\n' + json.program.map(x => obj_to_bts(x)).join('\n') + `\nCYC VALUE ${json.count} *;`;
}

bmgen_bts_converter['variable'] = function (json) {
    return `${json.name}`;
}

bmgen_bts_converter['channel'] = function (json) {
    return `${json.name}`;
}

bmgen_bts_converter['number'] = function (json) {
    return `${json.value}`;
}

bmgen_bts_converter['comment'] = function (json) {
    return `! ${json.text}`;
}

bmgen_bts_converter['label'] = function (json) {
    return `LABEL ${json.name}`;
}

function obj_to_bts(json) {
    if (typeof json === 'object' && json !== null) {
        return bmgen_bts_converter[json.type](json);
    } else {
        return `${json}`;
    }
}

function bmgen_to_bts(program) {
    return program.map(x => obj_to_bts(x)).join('\n') + '\nSTO;';
}

exports = { bmgen_to_bts };