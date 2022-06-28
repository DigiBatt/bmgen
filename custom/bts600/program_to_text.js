goog.module("BMGen3000.BTS600.ProgramToText");
let Parsetree = goog.require("BMGen3000.BTS600.Parsetree");

Parsetree.BTSVariable.prototype.toText = function () {
    return this.name;
}

Parsetree.BTSNumber.prototype.toText = function () {
    return String(this.value);
}

Parsetree.BTSMultiplication.prototype.toText = function () {
    return this.lhs.toText() + " " + this.rhs.toText();
}

Parsetree.BTSValue.prototype.toText = function () {
    return "VALUE " + this.numvalue.toText();
}

Parsetree.BTSCycleCount.prototype.toText = function () {
    return "VALUE " + this.numvalue.toText() + " *";
}

Parsetree.BTSAssignment.prototype.toText = function () {
    return "VALUE " + this.variable.toText() + " = " + this.numvalue.toText();
}

Parsetree.BTSGoto.prototype.toText = function () {
    return "GOTO " + this.label;
}

Parsetree.BTSError.prototype.toText = function () {
    return "ERR " + this.errnum;
}

Parsetree.BTSLimit.prototype.toText = function () {
    var action = "";
    if (this.action) {
        action = " " + this.action[0].toText();
    }
    return "LIMIT " + this.operator + " " + this.numvalue.toText();
}

Parsetree.BTSRegistration.prototype.toText = function () {
    return "REGISTRATION " + this.numvalue.toText();
}

Parsetree.BTSStatement.prototype.toText = function () {
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
    if (this.label) {
        text = `LABEL ${this.label}\n` + text;
    }
    return text;
}

Parsetree.BTSComment.prototype.toText = function () {
    return "! " + this.text;
}

Parsetree.BTSProgram.prototype.toText = function () {
    return this.lines.map(x => x.toText()).join("\n");
}
