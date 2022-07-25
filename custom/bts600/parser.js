goog.module("BMGen3000.BTS600.parser");

const Parsetree = goog.require("BMGen3000.BTS600.Parsetree");

function bts_parse_program(program) {
    var lines = [];
    const statements = program.split(';');
    for (var i = 0; i < statements.length; i++) {
        var stmt = statements[i].trim();
        var label = null;
        while (stmt.startsWith('!')) {
            var commentEnd = stmt.indexOf("\n");
            var comment = stmt.substring(0, commentEnd);
            stmt = stmt.substring(commentEnd + 1).trim();
            lines.push(bts_parse_comment(comment));
        }
        while (stmt.startsWith('LABEL')) {
            var labelEnd = stmt.indexOf("\n");
            label = stmt.substring(6, labelEnd).trim();
            stmt = stmt.substring(labelEnd + 1).trim();
        }
        if (stmt) {
            lines.push(bts_parse_statement(stmt, label));
        }
    }
    return new Parsetree.BTSProgram(lines);
}

function bts_parse_comment(comment) {
    comment = comment.trim();
    if (!comment.startsWith('!')) {
        throw new Error('Invalid comment');
    }
    return new Parsetree.BTSComment(comment.substring(1).trim());
}

function bts_parse_statement(statement, label) {
    var tokens = statement.trim().replace(/[\n\r]+/gm, ' ').replace(/ +/g, ' ').split(' ');
    const operator = tokens[0];
    var values = [];
    var limits = [];
    var registrations = [];
    var action = null;
    var arg = '';
    for (var i = tokens.length - 1; i > 0; i--) {
        const kw = tokens[i].toUpperCase();
        if (kw == 'REGISTRATION') {
            registrations.unshift(bts_parse_registration(arg));
            arg = '';
            action = null;
        }
        else if (kw == 'ACTION') {
            action = bts_parse_action(arg);
            arg = '';
        }
        else if (kw == 'LIMIT') {
            limits.unshift(bts_parse_limit(arg, action));
            arg = '';
            action = null;
        }
        else if (kw == 'VALUE') {
            values.unshift(bts_parse_value(arg));
            arg = '';
            action = null;
        } else {
            arg = tokens[i] + ' ' + arg;
        }
    }
    let bts_statement = new Parsetree.BTSStatement(operator, values, limits, registrations);
    if (label) {
        bts_statement.label = label;
    }
    return bts_statement;
}

function bts_parse_action(action) {
    const tokens = action.trim().split(' ');
    if (tokens[0].toUpperCase() == 'GOTO') {
        return new Parsetree.BTSGoto(tokens[1]);
    }
    else if (tokens[0].toUpperCase() == 'ERR') {
        return new Parsetree.BTSError(Number(tokens[1]));
    }
}

function bts_parse_limit(limit, action) {
    let condition;
    const parts = limit.trim().split('&');
    for (let i = 0; i < parts.length; i++) {
        let new_condition;
        const tokens = parts[i].trim().split(' ');
        if (tokens[1] === '=') {
            new_condition = new Parsetree.BTSLimitEqual(tokens[0], tokens[2]);
        } else {
            const operator = tokens[0];
            const numvalue = bts_parse_numvalue(tokens.slice(1).join(' '));
            new_condition = new Parsetree.BTSLimitSingleCondition(operator, numvalue);
        }
        if (condition) {
            condition = new Parsetree.BTSLimitAnd(condition, new_condition);
        } else {
            condition = new_condition;
        }
    }
    return new Parsetree.BTSLimit(condition, action);
}

function bts_parse_value(value) {
    const tokens = value.trim().split(' ');
    if (tokens[1] == '=') {
        const numvalue = bts_parse_numvalue(tokens.slice(2).join(' '));
        const variable = bts_parse_numvalue(tokens[0]);
        return new Parsetree.BTSAssignment(variable, numvalue);
    } else if (tokens[tokens.length - 1] == '*') {
        const numvalue = bts_parse_numvalue(tokens.slice(0, tokens.length - 1).join(' '));
        return new Parsetree.BTSCycleCount(numvalue);
    } else {
        const numvalue = bts_parse_numvalue(tokens.join(' '));
        return new Parsetree.BTSValue(numvalue);
    }
}

function bts_parse_numvalue(numvalue) {
    const tokens = numvalue.trim().split(' ');
    if (tokens.length > 1) {
        const lhs = bts_parse_numvalue(tokens[0]);
        const rhs = bts_parse_numvalue(tokens.slice(1, tokens.length).join(' '));
        return new Parsetree.BTSMultiplication(lhs, rhs);
    }
    else {
        const value = Number(tokens[0]);
        if (isNaN(value)) {
            return new Parsetree.BTSVariable(tokens[0]);
        } else {
            return new Parsetree.BTSNumber(value);
        }
    }
}

function bts_parse_registration(registration) {
    return new Parsetree.BTSRegistration(bts_parse_numvalue(registration));
}

exports = { bts_parse_program }