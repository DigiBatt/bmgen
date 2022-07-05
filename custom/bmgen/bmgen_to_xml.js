goog.module("BMGen3000.BMGenToXML");

function gen_xml_id() {
    const length = 20;
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    return result;
}

let bmgen_xml_converter = {};

bmgen_xml_converter['variable'] = function (x) {
    return `<block type="variable" id="${gen_xml_id()}"><field name="NAME">${x.name}</field></block>`;
}

bmgen_xml_converter['channel'] = function (x) {
    return `<block type="channel" id="${gen_xml_id()}"><field name="NAME">${x.name}</field></block>`;
}

bmgen_xml_converter['number'] = function (x) {
    return `<block type="number" id="${gen_xml_id()}"><field name="NUMBER">${x.value}</field></block>`;
}

bmgen_xml_converter['time'] = function (x) {
    return `<block type="time" id="${gen_xml_id()}"><field name="VALUE">${x.value}</field><field name="UNIT">${x.unit}</field></block>`;
}

bmgen_xml_converter['comparison'] = function (x) {
    return `<block type="comparison" id="${gen_xml_id()}"><value name="LHS">${bmgen_obj_to_xml(x.lhs)}</value><field name="OPERATOR">${bmgen_escape_xml(x.operator)}</field><value name="RHS">${bmgen_obj_to_xml(x.rhs)}</value></block>`;
}

bmgen_xml_converter['setvalue'] = function (x, next) {
    var xml = `<block type="setvalue" id="${gen_xml_id()}"><value name="VALUE">${bmgen_obj_to_xml(x.value)}</value><value name="CHANNEL">${bmgen_obj_to_xml(x.channel)}</value>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['setvalue_equal'] = function (x, next) {
    var xml = `<block type="assignment" id="${gen_xml_id()}"><value name="LHS">${bmgen_obj_to_xml(x.channel)}</value><value name="RHS">${bmgen_obj_to_xml(x.value)}</value>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['assignment'] = function (x, next) {
    var xml = `<block type="assignment" id="${gen_xml_id()}"><value name="LHS">${bmgen_obj_to_xml(x.lhs)}</value><value name="RHS">${bmgen_obj_to_xml(x.rhs)}</value>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}


bmgen_xml_converter['error'] = function (x) {
    return `<block type="action_error" id="${gen_xml_id()}"><field name="ERRNUM">${x.errnum}</field></block>`;
}

bmgen_xml_converter['limit'] = function (x, next) {
    if (x.action) {
        var xml = `<block type="limit_action" id="${gen_xml_id()}"><value name="CONDITION">${bmgen_obj_to_xml(x.condition)}</value><value name="ACTION">${bmgen_obj_to_xml(x.action)}</value>`;
    } else {
        var xml = `<block type="limit" id="${gen_xml_id()}"><value name="CONDITION">${bmgen_obj_to_xml(x.condition)}</value>`;
    }
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['cycle'] = function (x, next) {
    var xml = `<block type="function_cycle" id="${gen_xml_id()}"><field name="COUNT">${x.count}</field><statement name="ARGS">${bmgen_obj_list_to_xml(x.program)}</statement>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['function'] = function (x, next) {
    const blockname = `function_${x.name}`;
    if (blockname in bmgen_xml_converter) {
        return bmgen_xml_converter[blockname](x, next);
    }
    let xml;
    if (x.args.length > 0) {
        xml = `<block type="function" id="${gen_xml_id()}"><field name="NAME">${x.name}</field><statement name="ARGS">${bmgen_obj_list_to_xml(x.args)}</statement>`;
    } else {
        xml = `<block type="empty_function" id="${gen_xml_id()}"><field name="NAME">${x.name}</field>`;
    }
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['function_charge'] = function (x, next) {
    let xml = `<block type="function_charge" id="${gen_xml_id()}"><statement name="ARGS">${bmgen_obj_list_to_xml(x.args)}</statement>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['function_discharge'] = function (x, next) {
    let xml = `<block type="function_discharge" id="${gen_xml_id()}"><statement name="ARGS">${bmgen_obj_list_to_xml(x.args)}</statement>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['function_pause'] = function (x, next) {
    let xml = `<block type="function_pause" id="${gen_xml_id()}"><statement name="ARGS">${bmgen_obj_list_to_xml(x.args)}</statement>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['comment'] = function (x, next) {
    let xml = `<block type="comment" id="${gen_xml_id()}"><field name="TEXT">${x.text}</field>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['label'] = function (x, next) {
    let xml = `<block type="label" id="${gen_xml_id()}"><field name="LABEL">${x.name}</field>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['registration'] = function (x, next) {
    let xml = `<block type="registration" id="${gen_xml_id()}"><statement name="ARGS">${bmgen_obj_list_to_xml(x.args)}</statement>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['regname'] = function (x) {
    return `<block type="regname" id="${gen_xml_id()}"><field name="NAME">${x.name}</field></block>`;
}

bmgen_xml_converter['math'] = function (x, next) {
    var xml = `<block type="math" id="${gen_xml_id()}"><value name="LHS">${bmgen_obj_to_xml(x.lhs)}</value><value name="RHS">${bmgen_obj_to_xml(x.rhs)}</value><field name="OPERATOR">${bmgen_escape_xml(x.operator)}</field>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

bmgen_xml_converter['limit_global'] = bmgen_xml_converter['limit'];
bmgen_xml_converter['registration_global'] = bmgen_xml_converter['registration'];

function bmgen_obj_to_xml(json) {
    if (typeof json === 'object' && json !== null) {
        return bmgen_xml_converter[json.type](json);
    } else {
        return `${json}`;
    }
}

function bmgen_obj_list_to_xml(json) {
    var next = '';
    for (var i = json.length - 1; i >= 0; i--) {
        next = bmgen_xml_converter[json[i].type](json[i], next);
    }
    return next;
}

function bmgen_escape_xml(x) {
    return x.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function bmgen_to_xml(program) {
    const xml = bmgen_obj_list_to_xml(program);
    return '<xml xmlns="https://developers.google.com/blockly/xml">' + xml + '</xml>';
}

exports = { bmgen_to_xml };