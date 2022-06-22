BTSNumValue.prototype.toBM = function () {
    return this.toText();
}

BTSCycleCount.prototype.toBM = function () {
    return this.numvalue.toText() + " *";
}

BTSAssignment.prototype.toBM = function () {
    return this.variable.toText() + " = " + this.numvalue.toText();
}

BTSLimit.prototype.toBM = function () {
    const limit = this.operator + " " + this.numvalue.toText();
    var action = "";
    if (this.action) {
        action = this.action.toText();
    }
    return [limit, action];
}

BTSRegistration.prototype.toBM = function () {
    return this.numvalue.toText();
}

BTSValue.prototype.toBM = function () {
    return this.numvalue.toText();
}

BTSStatement.prototype.toBM = function (linenumber) {
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
    return `\t${linenumber}\t\t${this.operator}\t${value}\t${limit}\t${action}\t${registration}\n`;
}

BTSComment.prototype.toBM = function () {
    return `\t\t!\t${this.text}`;
}

BTSProgram.prototype.toBM = function () {
    var program = '';
    var linenumber = 1;
    for (var i = 0; i < this.lines.length; i++) {
        const line = this.lines[i];
        if (line instanceof BTSComment) {
            program += line.toBM(); + "\n";
        } else {
            program += line.toBM(linenumber);
            linenumber++;
        }
    }
    return program;
}
