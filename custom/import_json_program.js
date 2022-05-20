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

function json_chain_blocks(x) {

}

function json_numvalue_to_xml(x) {
    if (x.type == 'number') {
        return `<block type="math_number" id="${gen_xml_id()}"><field name="NUM">${x.value}</field></block>`;
    } else if (x.type == 'variable') {
        return `<block type="variable" id="${gen_xml_id()}"><field name="VARIABLE">${x.name}</field></block>`;
    }
}

function json_compare_to_xml(x) {
    const OPERATORS = { "<=": "LTE", ">=": "GTE", "<": "LT", ">": "GT" };
    const operator = OPERATORS[x.operator];
    const factor = json_numvalue_to_xml(x.value.lhs);
    const channel = `<block type="channel" id="${gen_xml_id()}"><field name="CHANNEL">${x.value.rhs.name}</field></block>`;
    return `<block type="compare" id="${gen_xml_id()}"><field name="OPERATOR">${operator}</field><value name="FACTOR">${factor}</value><value name="CHANNEL">${channel}</value></block>`;
}

function json_action_to_xml(x) {
    if (x.type == 'error') {
        return `<block type="err" id="${gen_xml_id()}"><field name="ERRNUM">${x.number}</field></block>`;
    }
}

function json_valueexpr_to_xml(x, next) {
    if (x.type == 'assignment') {
        var targetdef = {
            'type': 'variable',
            'name': x.target
        };
        var xml = `<block type="assignment" id="${gen_xml_id()}"><value name="LHS">${json_numvalue_to_xml(targetdef)}</value><field name="RHS">${x.value.value}</field>`;
        if (next) {
            xml += '<next>' + next + '</next>';
        }
        xml += "</block>";
        return xml;
    }
    return next;
}

function json_limit_to_xml(x, next) {
    var blocktype = 'limit';
    const has_action = ("type" in x.action);
    if (has_action) {
        blocktype = 'limit_action';
    }
    var xml = `<block type="${blocktype}" id="${gen_xml_id()}"><value name="EXPRESSION">` + json_compare_to_xml(x) + '</value>';
    if (has_action) {
        xml += '<statement name="ACTION">' + json_action_to_xml(x.action) + '</statement>';
    }
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

function json_args_to_xml(x) {
    var next = '';
    var xml = '';
    if (x.limit.length > 0) {
        for (var i = x.limit.length - 1; i >= 0; i--) {
            next = json_limit_to_xml(x.limit[i], next);
        }
        xml = '<statement name="LIMIT">' + next + '</statement>';
    }
    if (x.value.length > 0) {
        next = ''
        for (var i = x.value.length - 1; i >= 0; i--) {
            next = json_valueexpr_to_xml(x.value[i], next);
        }
        xml += '<statement name="VALUE">' + next + '</statement>';
    }
    return xml;
}

function json_stat_to_xml(x, next) {
    if (x.operator.startsWith('!')) {
        return next;
    } else {
        var xml = `<block type="${x.operator.toLowerCase()}" id="${gen_xml_id()}">` + json_args_to_xml(x.args);
        if (next) {
            xml += '<next>' + next + '</next>';
        }
        xml += '</block>';
        return xml;
    }
}

function json_program_to_xml(x) {
    var next = '';
    for (var i = x.statements.length - 1; i >= 0; i--) {
        next = json_stat_to_xml(x.statements[i], next);
    }
    return '<xml xmlns="https://developers.google.com/blockly/xml">' + next + '</xml>';
}

function import_json_program(file) {
    var x = JSON.parse(file);
    var xml = json_program_to_xml(x);
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'application/xml');
    workspace.clear();
    Blockly.Xml.domToWorkspace(doc.documentElement, workspace);
}