goog.module("BMGen3000.BMGenToBTS");

let bmgen_bts_converter = {};

const bmgen_function_map = {
    'pause': 'PAU',
    'charge': 'CHA',
    'discharge': 'DCH'
}

var bmgen_label_count = 0;
var bmgen_array_names = [];

bmgen_bts_converter['assignment'] = function (json) {
    return `SET VALUE ${obj_to_bts(json.lhs, json)} = ${obj_to_bts(json.rhs, json)};`;
}

bmgen_bts_converter['function'] = function (json) {
    var name = json.name;
    if (name in bmgen_function_map) {
        name = bmgen_function_map[name];
    }
    return name + ' ' + json.args.map(x => obj_to_bts(x, json)).join(' ') + ';';
}

bmgen_bts_converter['limit_global'] = function (json) {
    var text = 'SET LIMIT ' + obj_to_bts(json.condition, json);
    if (json.action) {
        text += ' ' + obj_to_bts(json.action, json);
    }
    text += ';';
    return text;
}

bmgen_bts_converter['limit'] = function (json) {
    var text = 'LIMIT ' + obj_to_bts(json.condition, json);
    if (json.action) {
        text += ' ' + obj_to_bts(json.action, json);
    }
    return text;
}

bmgen_bts_converter['comparison'] = function (json) {
    if (json.operator === '=') {
        return `${obj_to_bts(json.lhs, json)} = ${obj_to_bts(json.rhs, json)}`;
    } else {
        return `${json.operator} ${obj_to_bts(json.rhs, json)} ${obj_to_bts(json.lhs, json)}`;
    }
}

bmgen_bts_converter['error'] = function (json) {
    return `ACTION ERR ${json.errnum}`;
}

bmgen_bts_converter['goto'] = function (json) {
    return `ACTION GOTO ${json.label}`;
}

bmgen_bts_converter['setvalue'] = function (json) {
    return `VALUE ${obj_to_bts(json.value, json)} ${obj_to_bts(json.channel, json)}`;
}

bmgen_bts_converter['setvalue_equal'] = function (json) {
    return `VALUE ${obj_to_bts(json.value, json)} ${obj_to_bts(json.channel, json)}`;
}

bmgen_bts_converter['time'] = function (json) {
    return `> ${obj_to_bts(json.value, json)} ${json.unit}`;
}

bmgen_bts_converter['cycle'] = function (json) {
    return 'BEG;\n' + json.program.map(x => bts_postprocess(obj_to_bts(x, json))).join('\n') + `\nCYC VALUE ${json.count} *;`;
}

bmgen_bts_converter['while'] = function (json) {
    const label = `bmgen_${bmgen_label_count++}`;
    return `LABEL ${label}\n` + json.program.map(x => bts_postprocess(obj_to_bts(x))).join('\n') + `\nPAU LIMIT ${bts_postprocess(obj_to_bts(json.condition))} ACTION GOTO ${label} LIMIT 1 sec;`;
}

bmgen_bts_converter['for'] = function (json) {
    const label = `bmgen_${bmgen_label_count++}`;
    let text = bts_postprocess(obj_to_bts(json.init_statement)) + '\n';
    text += `LABEL ${label}\n`;
    text += json.program.map(x => bts_postprocess(obj_to_bts(x))).join('\n');
    text += '\n' + bts_postprocess(obj_to_bts(json.loop_statement));
    text += `\nPAU LIMIT ${bts_postprocess(obj_to_bts(json.condition))} ACTION GOTO ${label} LIMIT 1 sec;`;
    return text;
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

bmgen_bts_converter['registration'] = function (json) {
    return json.args.map(x => 'REGISTRATION ' + obj_to_bts(x, json)).join(' ');
}

bmgen_bts_converter['registration_global'] = function (json) {
    return 'SET ' + json.args.map(x => 'REGISTRATION ' + obj_to_bts(x, json)).join(' ') + ';';
}

bmgen_bts_converter['regname'] = function (json) {
    return `${json.name}`;
}

bmgen_bts_converter['math'] = function (json) {
    if (json.operator === '+=') {
        return `ADD VALUE ${obj_to_bts(json.lhs, json)} VALUE ${obj_to_bts(json.rhs, json)};`;
    } else if (json.operator === '-=') {
        return `SUB VALUE ${obj_to_bts(json.lhs, json)} VALUE ${obj_to_bts(json.rhs, json)};`;
    } else {
        console.error('unknown operator');
    }
}

bmgen_bts_converter['limit_and'] = function (json) {
    return `${obj_to_bts(json.lhs, json)} & ${obj_to_bts(json.rhs, json)}`;
}

bmgen_bts_converter['array_init'] = function (json) {
    const arrayNum = bmgen_array_names.length;
    bmgen_array_names.push(json.array);
    return `SET VALUE ${json.array}_IV = ${123454321 + arrayNum} VALUE ${json.array}_Val = 0 ${json.values.map((v, i) => `VALUE ${json.array}_${i} = ${v}`).join(' ')};`;
}

bmgen_bts_converter['array_access'] = function (json) {
    const arrayNum = bmgen_array_names.indexOf(json.array);
    if (arrayNum < 0) {
        throw new Error(`Array ${json.array} was not initialized`);
    }
    let wrapper = '';
    if (json.parent.type === 'assignment' && json.parent.lhs === json) {
        wrapper = `#pre{SET VALUE idx = ${obj_to_bts(json.index, json)};\nADD VALUE idx VALUE ${arrayNum * 1000};} #post{PAU LIMIT > idx arrSET;}`;
    } else {
        wrapper = `#pre{SET VALUE idx = ${obj_to_bts(json.index, json)};\nADD VALUE idx VALUE ${arrayNum * 1000};\nPAU LIMIT > idx arrGET;}`;
    }
    return `${json.array}_Val ${wrapper}`;
}

function obj_to_bts(json, parent) {
    if (typeof json === 'object' && json !== null) {
        if (json.type in bmgen_bts_converter) {
            json.parent = parent;
            return bmgen_bts_converter[json.type](json);
        } else {
            throw new Error(`Missing conversion function for type ${json.type}`);
        }
    } else {
        return `${json}`;
    }
}

function bts_postprocess(line) {
    let pre = '';
    let post = '';
    const pattern = /#([a-zA-Z]+){([^}]*)}/g;
    const matches = line.matchAll(pattern);
    for (const m of matches) {
        if (m[1] === 'pre') {
            pre += m[2] + '\n';
        } else if (m[1] === 'post') {
            post += '\n' + m[2];
        } else {
            throw new Error(`Unknown postprocessing directive #${m[1]}`);
        }
    }
    return pre + line.replace(pattern, '') + post;
}

function bmgen_to_bts(program) {
    bmgen_label_count = 0;
    bmgen_array_names = [];
    return program.map(x => bts_postprocess(obj_to_bts(x, program))).join('\n') + '\nSTO;';
}

exports = { bmgen_to_bts };