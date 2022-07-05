goog.module("BMGen3000.BTS600.ProgramToBM");
let Parsetree = goog.require("BMGen3000.BTS600.Parsetree");

Parsetree.BTSNumValue.prototype.toBM = function () {
    return this.toText();
}

Parsetree.BTSCycleCount.prototype.toBM = function () {
    return this.numvalue.toText() + " *";
}

Parsetree.BTSAssignment.prototype.toBM = function () {
    return this.variable.toText() + " = " + this.numvalue.toText();
}

Parsetree.BTSLimitSingleCondition.prototype.toBM = function () {
    return this.toText();
}

Parsetree.BTSLimitAnd.prototype.toBM = function () {
    return this.lhs.toText() + " &\\r\\n" + this.rhs.toText();
}

Parsetree.BTSLimit.prototype.toBM = function () {
    const limit = this.condition.toBM();
    const linebreaks = (limit.match(/\\r\\n/g) || []).length;
    var action = "";
    if (this.action) {
        action = "\\r\\n".repeat(linebreaks) + this.action.toText();
    }
    return [limit, action];
}

Parsetree.BTSRegistration.prototype.toBM = function () {
    return this.numvalue.toText();
}

Parsetree.BTSValue.prototype.toBM = function () {
    return this.numvalue.toText();
}

Parsetree.BTSStatement.prototype.toBM = function (linenumber) {
    const value = this.values ? this.values.map(x => x.toBM()).join("\\r\\n") : "";
    const registration = this.registrations ? this.registrations.map(x => x.toBM()).join("\\r\\n") : "";
    var limit = [];
    var action = [];
    if (this.limits) {
        for (var i = 0; i < this.limits.length; i++) {
            var ret = this.limits[i].toBM();
            limit[i] = ret[0];
            action[i] = ret[1];
        }
    }
    limit = limit.join("\\r\\n");
    action = action.join("\\r\\n");
    const label = this.label ? this.label : '';
    return `\t${linenumber}\t${label}\t${this.operator}\t${value}\t${limit}\t${action}\t${registration}\n`;
}

Parsetree.BTSComment.prototype.toBM = function () {
    return `\t\t!\t${this.text}`;
}

Parsetree.BTSProgram.prototype.toBM = function () {
    var program = '';
    var linenumber = 1;
    for (var i = 0; i < this.lines.length; i++) {
        const line = this.lines[i];
        if (line instanceof Parsetree.BTSComment) {
            program += line.toBM(); + "\n";
        } else {
            program += line.toBM(linenumber);
            linenumber++;
        }
    }
    return program;
}
