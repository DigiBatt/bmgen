BTSNumValue.prototype.toTable = function () {
    return this.toText();
}

BTSCycleCount.prototype.toTable = function () {
    return this.numvalue.toText() + " *";
}

BTSAssignment.prototype.toTable = function () {
    return this.variable.toText() + " = " + this.numvalue.toText();
}

BTSLimit.prototype.toTable = function () {
    const limit = this.operator + " " + this.numvalue.toText();
    var action = "";
    if (this.action) {
        action = this.action[0].toText();
    }
    return [limit, action];
}

BTSRegistration.prototype.toTable = function () {
    return this.numvalue.toText();
}

BTSStatement.prototype.toTable = function (linenumber) {
    const value = this.values ? this.values.map(x => x.toTable()).join("<br>") : "";
    const registration = this.registrations ? this.registrations.map(x => x.toTable()).join("<br>") : "";
    var limit = [];
    var action = [];
    if (this.limits) {
        for (var i = 0; i < this.limits.length; i++) {
            var ret = this.limits[i].toTable();
            limit[i] = ret[0];
            action[i] = ret[1];
        }
    }
    limit = limit.join("<br>");
    action = action.join("<br>");
    return `<tr><td>${linenumber}</td><td></td><td>${this.operator}</td><td>${value}</td><td>${limit}</td><td>${action}</td><td>${registration}</td></tr>\n`;
}

BTSComment.prototype.toTable = function () {
    return `<tr><td></td><td colspan="6">! ${this.text}</td></tr>`;
}

BTSProgram.prototype.toTable = function () {
    var table = '<table>\n<tr><th>Step</th><th>Label</th><th>Operator</th><th>Value</th><th>Limit</th><th>Action</th><th>Registration</th></tr>\n'
    var linenumber = 1;
    for (var i = 0; i < this.lines.length; i++) {
        const line = this.lines[i];
        if (line instanceof BTSComment) {
            table += line.toTable(); + "\n";
        } else {
            table += line.toTable(linenumber);
            linenumber++;
        }
    }
    table += '</table>';
    return table;
}
