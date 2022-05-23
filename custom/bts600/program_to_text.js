BTSVariable.prototype.toText = function () {
    return this.name;
}

BTSNumber.prototype.toText = function () {
    return String(this.value);
}

BTSMultiplication.prototype.toText = function () {
    return this.lhs.toText() + " " + this.rhs.toText();
}

BTSCycleCount.prototype.toText = function () {
    return "VALUE " + this.numvalue.toText() + " *";
}

BTSAssignment.prototype.toText = function () {
    return "VALUE " + this.variable.toText() + " = " + this.numvalue.toText();
}

BTSGoto.prototype.toText = function () {
    return "GOTO " + this.label;
}

BTSError.prototype.toText = function () {
    return "ERR " + this.errnum;
}

BTSLimit.prototype.toText = function () {
    var action = "";
    if (this.action) {
        action = " " + this.action[0].toText();
    }
    return "LIMIT " + this.operator + " " + this.numvalue.toText();
}

BTSRegistration.prototype.toText = function () {
    return "REGISTRATION " + this.numvalue.toText();
}

BTSStatement.prototype.toText = function () {
    var text = this.operator;
    const sep = '\n' + ' '.repeat(this.operator.length + 1);
    var prefix = " ";
    if (this.values) {
        const values = this.values.map(x => x.toText()).join(sep);
        if (values) {
            text += prefix + values;
            prefix = sep;
        }
    }
    if (this.limits) {
        const limits = this.limits.map(x => x.toText()).join(sep);
        if (limits) {
            text += prefix + limits;
            prefix = sep;
        }
    }
    if (this.registrations) {
        const registrations = this.registrations.map(x => x.toText()).join(sep);
        if (registrations) {
            text += prefix + registrations;
        }
    }
    text += ";";
    return text;
}

BTSComment.prototype.toText = function () {
    return "! " + this.text;
}

BTSProgram.prototype.toText = function () {
    return this.lines.map(x => x.toText()).join("\n");
}
