function bts_parse_program(program) {
    var lines = [];
    const statements = program.split(';');
    for (var i = 0; i < statements.length; i++) {
        var stmt = statements[i].trim();
        while (stmt.startsWith('!')) {
            var commentEnd = stmt.indexOf("\n");
            var comment = stmt.substring(0, commentEnd);
            stmt = stmt.substring(commentEnd + 1);
            lines.push(bts_parse_comment(comment));
        }
        if (stmt) {
            lines.push(bts_parse_statement(stmt));
        }
    }
    return new BTSProgram(lines);
}

function bts_parse_comment(comment) {
    comment = comment.trim();
    if (!comment.startsWith('!')) {
        error('Invalid comment');
    }
    return new BTSComment(comment.substring(1).trim());
}

function bts_parse_statement(statement) {
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
    return new BTSStatement(operator, values, limits, registrations);
}

function bts_parse_action(action) {
    const tokens = action.trim().split(' ');
    if (tokens[0].toUpperCase() == 'GOTO') {
        return new BTSGoto(tokens[1]);
    }
    else if (tokens[0].toUpperCase() == 'ERR') {
        return new BTSError(Number(tokens[1]));
    }
}

function bts_parse_limit(limit, action) {
    const tokens = limit.trim().split(' ');
    const operator = tokens[0];
    const numvalue = bts_parse_numvalue(tokens.slice(1).join(' '));
    return new BTSLimit(operator, numvalue, action);
}

function bts_parse_value(value) {
    const tokens = value.trim().split(' ');
    if (tokens[1] == '=') {
        const numvalue = bts_parse_numvalue(tokens.slice(2).join(' '));
        const variable = bts_parse_numvalue(tokens[0]);
        return new BTSAssignment(variable, numvalue);
    } else if (tokens[tokens.length - 1] == '*') {
        const numvalue = bts_parse_numvalue(tokens.slice(0, tokens.length - 1).join(' '));
        return new BTSCycleCount(numvalue);
    } else {
        const numvalue = bts_parse_numvalue(tokens.join(' '));
        return new BTSValue(numvalue);
    }
}

function bts_parse_numvalue(numvalue) {
    const tokens = numvalue.trim().split(' ');
    if (tokens.length > 1) {
        const lhs = bts_parse_numvalue(tokens[0]);
        const rhs = bts_parse_numvalue(tokens.slice(1, tokens.length).join(' '));
        return new BTSMultiplication(lhs, rhs);
    }
    else {
        const value = Number(tokens[0]);
        if (isNaN(value)) {
            return new BTSVariable(tokens[0]);
        } else {
            return new BTSNumber(value);
        }
    }
}

function bts_parse_registration(registration) {
    return new BTSRegistration(bts_parse_numvalue(registration));
}