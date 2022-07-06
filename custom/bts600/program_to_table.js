goog.module("BMGen3000.BTS600.ProgramToTable");
let Parsetree = goog.require("BMGen3000.BTS600.Parsetree");

Parsetree.BTSNumValue.prototype.toTable = function () {
    return this.toText();
}

Parsetree.BTSCycleCount.prototype.toTable = function () {
    return this.numvalue.toText() + " *";
}

Parsetree.BTSAssignment.prototype.toTable = function () {
    return this.variable.toText() + " = " + this.numvalue.toText();
}

Parsetree.BTSValue.prototype.toTable = function () {
    return this.numvalue.toText();
}

Parsetree.BTSLimitCondition.prototype.toTable = function () {
    return this.toText();
}

Parsetree.BTSLimitAnd.prototype.toTable = function () {
    return this.lhs.toText() + " &<br>" + this.rhs.toText();
}

Parsetree.BTSLimit.prototype.toTable = function () {
    const limit = this.condition.toTable();
    const linebreaks = (limit.match(/<br>/g) || []).length;
    var action = "";
    if (this.action) {
        action = '<br>'.repeat(linebreaks) + this.action.toText();
    }
    return [limit, action];
}

Parsetree.BTSRegistration.prototype.toTable = function () {
    return this.numvalue.toText();
}

Parsetree.BTSStatement.prototype.toTable = function (linenumber) {
    if (this.values) {
        for (const v of this.values) {
            if (!(v instanceof Parsetree.BTSNode)) {
                console.log(`Line ${linenumber} (${this.operator}): no BTSNode`);
                console.log(v);
            }
            if (!('toTable' in v)) {
                console.log(`Line ${linenumber} (${this.operator}): no toTable function`);
                console.log(v);
            }
        }
    }
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
    const label = this.label ? this.label : '';
    return `<tr><td>${linenumber}</td><td>${label}</td><td>${this.operator}</td><td>${value}</td><td>${limit}</td><td>${action}</td><td>${registration}</td></tr>\n`;
}

Parsetree.BTSComment.prototype.toTable = function () {
    return `<tr><td></td><td>!</td><td colspan="5" style="text-align: left;"> ${this.text}</td></tr>`;
}

Parsetree.BTSProgram.prototype.toTable = function () {
    var table = '<table>\n<tr><th>Step</th><th>Label</th><th>Operator</th><th>Value</th><th>Limit</th><th>Action</th><th>Registration</th></tr>\n'
    var linenumber = 1;
    for (var i = 0; i < this.lines.length; i++) {
        const line = this.lines[i];
        if (line instanceof Parsetree.BTSComment) {
            table += line.toTable();
        } else {
            table += line.toTable(linenumber);
            linenumber++;
        }
    }
    table += '</table>';
    return table;
}
