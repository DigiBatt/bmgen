{

class BTSNode {}

class BTSProgram extends BTSNode {
	constructor(lines) {
    	super();
		this.lines = lines;
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

class BTSValue extends BTSNode {
	constructor(numvalue) {
		super();
		this.numvalue = numvalue;
	}
}

class BTSAssignment extends BTSNode {
	constructor(ID_value, numvalue_value) {
		super();
		this.ID_value = ID_value;
		this.numvalue_value = numvalue_value;
	}
}

class BTSCycleCount extends BTSValue {
	constructor(numvalue_value) {
		super(numvalue_value);
	}
}

class BTSNumValue extends BTSNode {
	constructor(atomicvalue_value) {
		super();
		this.atomicvalue_value = atomicvalue_value;
	}
}

class BTSMultiplication extends BTSNumValue {
	constructor(atomicvalue_value, variable_value) {
		super(atomicvalue_value);
		this.variable_value = variable_value;
	}
}

class BTSAtomicValue extends BTSNode { }

class BTSVariable extends BTSAtomicValue {
	constructor(ID_value) {
		super();
		this.ID_value = ID_value;
	}
}

class BTSFloat extends BTSAtomicValue {
	constructor(FLOAT_value) {
		super();
		this.FLOAT_value = FLOAT_value;
	}
}

class BTSLimit extends BTSNode {
	constructor(COMP_value, numvalue_value, action_value) {
		super();
		this.COMP_value = COMP_value;
		this.numvalue_value = numvalue_value;
		this.action_value = action_value;
	}
}

class BTSAction { }

class BTSError extends BTSAction {
	constructor(FLOAT_value) {
		super();
		this.FLOAT_value = FLOAT_value;
	}
}

class BTSGoto extends BTSAction {
	constructor(ID_value) {
		super();
		this.ID_value = ID_value;
	}
}

class BTSRegistration {
	constructor(numvalue_value) {
		this.numvalue_value = numvalue_value;
	}
}

}

BTSProgram =
	lines:(BTSLine _)* { return new BTSProgram(lines.map(x => x[0])); }

BTSLine =
	BTSSet
	/ BTSStatement
    / BTSComment
    
BTSSet =
	KW_SET _ assignments:(BTSAssignment _)* _ limits:(BTSLimit _)* _ registrations:(BTSRegistration _)* _ SEMICOLON { return new BTSStatement("SET", assignments.map(x => x[0]), limits.map(x => x[0]), registrations.map(x => x[0])); }
    
BTSStatement =
	operator:ID _ values:(BTSValue _)* _ limits:(BTSLimit _)* _ registrations:(BTSRegistration _)* _ SEMICOLON { return new BTSStatement(operator, values.map(x => x[0]), limits.map(x => x[0]), registrations.map(x => x[0])); }
	
BTSComment =
    comment:COMMENT { return new BTSComment(comment); }

BTSValue =
    BTSCycleCount
	/ KW_VALUE _ numvalue:BTSNumValue { return new BTSValue(numvalue); }
    
BTSAssignment =
	KW_VALUE _ variable:BTSVariable _ ASSIGN _ numvalue:BTSFloat { return new BTSAssignment(variable, numvalue); }
    
BTSCycleCount =
	KW_VALUE _ numvalue:BTSNumValue _ MATHMUL { return new BTSCycleCount(numvalue); }

BTSNumValue =
	BTSMultiplication
	/ atomicValue:BTSAtomicValue { return new BTSNumValue(atomicValue); }

BTSMultiplication =
	atomicValue:BTSAtomicValue _ variable:BTSVariable { return new BTSMultiplication(atomicValue, variable); }

BTSAtomicValue =
	BTSVariable
    / BTSFloat
    
BTSVariable = 
	value:ID { return new BTSVariable(value); }
    
BTSFloat =
	value:FLOAT { return new BTSFloat(value); }

BTSLimit =
	KW_LIMIT _ comp:COMP _ numvalue:BTSNumValue _ action:BTSAction { return new BTSLimit(comp, numvalue, action); }
	/ KW_LIMIT _ comp:COMP _ numvalue:BTSNumValue { return new BTSLimit(comp, numvalue); }

BTSAction =
	BTSError
    / BTSGoto
    
BTSError =
	KW_ACTION _ KW_ERR _ number:BTSFloat { return new BTSError(number); }
    
BTSGoto =
	KW_ACTION _ KW_GOTO _ label:ID { return new BTSGoto(label); }

BTSRegistration =
	KW_REGISTRATION _ numvalue:BTSNumValue { return new BTSRegistration(numvalue); }

COMMENT = $([ \t]*"!"[^\n]*)

KW_VALUE = $("VALUE"i)

KW_LIMIT = $("LIMIT"i)

KW_ACTION = $("ACTION"i)

KW_GOTO = $("GOTO"i)

KW_ERR = $("ERR"i)

KW_REGISTRATION = $("REGISTRATION"i)

KW_SET = $("SET"i)

FLOAT = $("-"?[0-9]+(.[0-9]+)?)

ID = $([A-Za-z][A-Za-z0-9]*)

COMP = $([><]"="?)

ASSIGN = $("=")

MATHMUL = $([*])

SEMICOLON = $([;])

_ = $([ \t\r\n]*)