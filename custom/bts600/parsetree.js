class BTSNode { }

class BTSNumValue extends BTSNode { }

class BTSVariable extends BTSNumValue {
    constructor(name) {
        super();
        this.name = name;
    }
}

class BTSNumber extends BTSNumValue {
    constructor(value) {
        super();
        this.value = value;
    }
}

class BTSMultiplication extends BTSNumValue {
    constructor(lhs, rhs) {
        super();
        this.lhs = lhs;
        this.rhs = rhs;
    }
}

class BTSValue extends BTSNode {
    constructor(numvalue) {
        super();
        this.numvalue = numvalue;
    }
}

class BTSCycleCount extends BTSValue {
    constructor(numvalue) {
        super(numvalue);
    }
}

class BTSAssignment extends BTSValue {
    constructor(variable, numvalue) {
        super(numvalue);
        this.variable = variable;
    }
}

class BTSAction extends BTSNode { }

class BTSGoto extends BTSAction {
    constructor(label) {
        super();
        this.label = label;
    }
}

class BTSError extends BTSAction {
    constructor(errnum) {
        super();
        this.errnum = errnum;
    }
}

class BTSLimit extends BTSNode {
    constructor(operator, numvalue, action) {
        super();
        this.operator = operator;
        this.numvalue = numvalue;
        this.action = action;
    }
}

class BTSRegistration extends BTSNode {
    constructor(numvalue) {
        super();
        this.numvalue = numvalue;
    }
}

class BTSLine extends BTSNode { }

class BTSStatement extends BTSLine {
    constructor(operator, values, limits, registrations) {
        super();
        this.operator = operator;
        this.values = values;
        this.limits = limits;
        this.registrations = registrations;
    }
}

class BTSComment extends BTSLine {
    constructor(text) {
        super();
        this.text = text;
    }
}

class BTSProgram extends BTSNode {
    constructor(lines) {
        super();
        this.lines = lines;
    }
}