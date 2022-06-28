goog.module("BMGen3000.BTS600.Simplify");
let { BTSProgram } = goog.require("BMGen3000.BTS600.Parsetree");

BTSProgram.prototype.simplify = function () {
    // combine SET statements
    var prev_set_value = false;
    var prev_set_limit = false;
    for (var i = this.lines.length - 1; i >= 0; i--) {
        var curr_set_value = false;
        var curr_set_limit = false;
        const line = this.lines[i]
        if (line.operator == 'SET') {
            if (line.values.length > 0 && line.limits.length == 0) {
                if (prev_set_value) {
                    line.values = line.values.concat(this.lines[i + 1].values);
                    this.lines[i + 1] = null;
                }
                curr_set_value = true;
            }
            else if (line.values.length == 0 && line.limits.length > 0) {
                if (prev_set_limit) {
                    line.limits = line.limits.concat(this.lines[i + 1].limits);
                    this.lines[i + 1] = null;
                }
                curr_set_limit = true;
            }
        }
        prev_set_value = curr_set_value;
        prev_set_limit = curr_set_limit;
    }
    this.lines = this.lines.filter(function (value, index, arr) { return value !== null });
    return this;
}