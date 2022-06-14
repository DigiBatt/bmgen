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

function numvalue_to_xml(x) {
    if (x instanceof BTSNumber) {
        return `<block type="math_number" id="${gen_xml_id()}"><field name="NUM">${x.value}</field></block>`;
    } else if (x instanceof BTSVariable) {
        return `<block type="variable" id="${gen_xml_id()}"><field name="VARIABLE">${x.name}</field></block>`;
    } else if (x instanceof BTSMultiplication) {
        return `<block type="factor" id="${gen_xml_id()}"><value name="FACTOR">${numvalue_to_xml(x.lhs)}</value><value name="VALUE">${numvalue_to_xml(x.rhs)}</value></block>`;
    }
}

function compare_to_xml(x) {
    const OPERATORS = { "<=": "LTE", ">=": "GTE", "<": "LT", ">": "GT" };
    const operator = OPERATORS[x.operator];
    const factor = numvalue_to_xml(x.numvalue.lhs);
    const channel = `<block type="channel" id="${gen_xml_id()}"><field name="CHANNEL">${x.numvalue.rhs.name}</field></block>`;
    return `<block type="compare" id="${gen_xml_id()}"><field name="OPERATOR">${operator}</field><value name="FACTOR">${factor}</value><value name="CHANNEL">${channel}</value></block>`;
}

function action_to_xml(x) {
    if (x instanceof BTSError) {
        return `<block type="err" id="${gen_xml_id()}"><field name="ERRNUM">${x.errnum}</field></block>`;
    }
}

function value_to_xml(x, next) {
    var xml = "";
    if (x instanceof BTSAssignment) {
        xml = `<block type="assignment" id="${gen_xml_id()}"><value name="LHS">${numvalue_to_xml(x.variable)}</value><field name="RHS">${x.numvalue.value}</field>`;
        if (next) {
            xml += '<next>' + next + '</next>';
        }
        xml += "</block>";
    }
    else if (x instanceof BTSCycleCount) {
        xml = x.numvalue.value;
    }
    else {
        xml = numvalue_to_xml(x.numvalue);
    }
    return xml;
}

function limit_to_xml(x, next) {
    var blocktype = 'limit';
    if (x.action) {
        blocktype = 'limit_action';
    }
    var xml = `<block type="${blocktype}" id="${gen_xml_id()}"><value name="EXPRESSION">` + compare_to_xml(x) + '</value>';
    if (x.action) {
        xml += '<statement name="ACTION">' + action_to_xml(x.action) + '</statement>';
    }
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += "</block>";
    return xml;
}

function args_to_xml(x) {
    var next = '';
    var xml = '';
    if (x.limits.length > 0) {
        for (var i = x.limits.length - 1; i >= 0; i--) {
            next = limit_to_xml(x.limits[i], next);
        }
        xml = '<statement name="LIMIT">' + next + '</statement>';
    }
    if (x.values.length > 0) {
        next = ''
        for (var i = x.values.length - 1; i >= 0; i--) {
            next = value_to_xml(x.values[i], next);
        }
        xml += '<statement name="VALUE">' + next + '</statement>';
    }
    return xml;
}

function statement_to_xml(x, next) {
    var xml = `<block type="${x.operator.toLowerCase()}" id="${gen_xml_id()}">` + args_to_xml(x);
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += '</block>';
    return xml;
}

function comment_to_xml(x, next) {
    var xml = `<block type="comment" id="${gen_xml_id()}"><field name="COMMENT">${x.text}</field>`;
    if (next) {
        xml += '<next>' + next + '</next>';
    }
    xml += '</block>';
    return xml;
}

function line_to_xml(x, next) {
    if (x instanceof BTSComment) {
        return comment_to_xml(x, next);
    } else {
        return statement_to_xml(x, next);
    }
}

function program_to_xml(x) {
    var next = '';
    for (var i = x.lines.length - 1; i >= 0; i--) {
        next = line_to_xml(x.lines[i], next);
    }
    return '<xml xmlns="https://developers.google.com/blockly/xml">' + next + '</xml>';
}

function import_text_program(file) {
    var program = bts_parse_program(file);
    var xml = program_to_xml(program);
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'application/xml');
    workspace.clear();
    Blockly.Xml.domToWorkspace(doc.documentElement, workspace);
}