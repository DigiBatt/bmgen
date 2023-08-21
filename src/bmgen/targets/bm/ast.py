from typing import List
from dataclasses import dataclass, field
from bmgen.targets.bm.helper.compare import compare
from bmgen.targets.bm.helper.cast import autocast
import bmgen.targets.bm as bm


class BMNode:
    def toText(self):
        raise NotImplementedError()

    def toTable(self):
        return self.toText()


class BMNumValue(BMNode):
    def toText(self):
        raise NotImplementedError()

    def __mul__(self, other: "BMVariable"):
        return BMMultiplication(numvalue=self, variable=other)


@compare
@dataclass
class BMVariable(BMNumValue):
    name: str

    def toText(self):
        return self.name

    @autocast("other")
    def __compare__(self, other: BMNumValue, operator: str):
        return BMLimitCompare(lhs=self, rhs=other, operator=operator)

    @autocast()
    def __iadd__(self, other: BMNumValue):
        bm.generator.add(BMStatement(operator="ADD", values=[self, other]))
        return self


@dataclass
class BMNumber(BMNumValue):
    value: float

    def toText(self):
        return str(self.value)


@dataclass
class BMValue(BMNode):
    numvalue: BMNumValue

    def toText(self):
        raise NotImplementedError()


@dataclass
class BMMultiplication(BMValue):
    variable: BMVariable

    def toText(self):
        return self.numvalue.toText() + " " + self.variable.toText()


@dataclass
class BMCycleCount(BMValue):
    def toText(self):
        return self.numvalue.toText() + " *"


@dataclass
class BMAssignment(BMValue):
    variable: BMVariable

    def toText(self):
        return self.variable.toText() + " = " + self.numvalue.toText()


@dataclass
class BMAction(BMNode):
    pass

    def toText(self):
        raise NotImplementedError()


@dataclass
class BMGoto(BMAction):
    label: str

    def toText(self):
        return "GOTO " + self.label


@dataclass
class BMError(BMAction):
    errnum: int

    def toText(self):
        return "ERR " + str(self.errnum)


class BMLimitCondition(BMNode):
    pass

    def toText(self):
        raise NotImplementedError()


@dataclass
class BMLimitCompare(BMLimitCondition):
    lhs: BMNumValue
    rhs: BMNumValue
    operator: str

    def __post_init__(self):
        if isinstance(self.lhs, BMVariable) and self.lhs.name == "A":
            if (
                isinstance(self.rhs, BMMultiplication)
                and self.rhs.variable.name == "ACn1"
            ):
                self.lhs = self.rhs.variable
                self.rhs = self.rhs.numvalue

    def toText(self):
        if self.operator == "==":
            return self.lhs.toText() + " = " + self.rhs.toText()
        else:
            return self.operator + " " + self.rhs.toText() + " " + self.lhs.toText()


@dataclass
class BMLimitAnd(BMLimitCondition):
    lhs: BMLimitCondition
    rhs: BMLimitCondition

    def toReadable(self):
        return self.lhs.toText() + " & " + self.rhs.toText()

    def toText(self):
        return self.lhs.toText() + " &\\r\\n " + self.rhs.toText()

    def toTable(self):
        return self.lhs.toText() + " &<br>" + self.rhs.toText()


@dataclass
class BMLimitTime(BMLimitCondition):
    value: BMNumValue
    unit: str

    def toText(self):
        return self.value.toText() + " " + self.unit


@dataclass
class BMLimit(BMNode):
    condition: BMLimitCondition
    action: BMAction | None = None

    def toText(self):
        condition = self.condition.toText()
        linebreaks = condition.count("\\r\\n")
        action = ""
        if self.action:
            action = "\\r\\n" * linebreaks + self.action.toText()
        return (condition, action)

    def toReadable(self):
        if self.action:
            return (
                "LIMIT " + self.condition.toText() + " ACTION " + self.action.toText()
            )
        else:
            return "LIMIT " + self.condition.toText()

    def toTable(self):
        condition = self.condition.toTable()
        linebreaks = condition.count("<br>")
        action = ""
        if self.action:
            action = "<br>" * linebreaks + self.action.toTable()
        return (condition, action)


@dataclass
class BMRegistration(BMNode):
    numvalue: BMNumValue

    def toText(self):
        return self.numvalue.toText()


class BMLine(BMNode):
    pass


# needs to be comined with the next statement before output is generated
@dataclass
class BMLabel(BMLine):
    label: str


@dataclass
class BMStatement(BMLine):
    operator: str
    values: List[BMValue] = field(default_factory=list)
    limits: List[BMLimit] = field(default_factory=list)
    registrations: List[BMRegistration] = field(default_factory=list)
    label: str | None = None

    def toText(self, linenumber):
        value = "\\r\\n".join([v.toText() for v in self.values])
        registration = "\\r\\n".join([r.toText() for r in self.registrations])
        label = self.label if self.label else ""
        if self.limits:
            limit, action = zip(*[l.toText() for l in self.limits])
        else:
            limit = ""
            action = ""
        limit = "\\r\\n".join(limit)
        action = "\\r\\n".join(action)
        return f"\t{linenumber}\t{label}\t{self.operator}\t{value}\t{limit}\t{action}\t{registration}\n"

    def toTable(self, linenumber):
        value = "<br>".join([v.toTable() for v in self.values])
        registration = "<br>".join([r.toTable() for r in self.registrations])
        label = self.label if self.label else ""
        if self.limits:
            limit, action = zip(*[l.toTable() for l in self.limits])
        else:
            limit = ""
            action = ""
        limit = "<br>".join(limit)
        action = "<br>".join(action)
        return f"<tr><td>{linenumber}</td><td>{label}</td><td>{self.operator}</td><td>{value}</td><td>{limit}</td><td>{action}</td><td>{registration}</td></tr>\n"


@dataclass
class BMComment(BMLine):
    text: str

    def toText(self):
        # return f"\t\t!\t{self.text}\n
        return ""

    def toTable(self):
        return f'<tr><td></td><td>!</td><td colspan="5" style="text-align: left;">{self.text}</td></tr>'


@dataclass
class BMProgram(BMNode):
    lines: List[BMLine] = field(default_factory=list)

    def toText(self):
        program = ""
        linenumber = 1
        for i in range(len(self.lines)):
            line = self.lines[i]
            if not line:
                continue
            if isinstance(line, BMComment):
                program += line.toText()
            else:
                program += line.toText(linenumber)
                linenumber += 1
        return program

    def toTable(self):
        table = '<html><head><style type="text/css">table, th, td { border: 1px solid black; border-collapse: collapse; vertical-align: top; text-align: center; }</style></head><body>'
        table += "<table>\n<tr><th>Step</th><th>Label</th><th>Operator</th><th>Value</th><th>Limit</th><th>Action</th><th>Registration</th></tr>\n"
        linenumber = 1
        for i in range(len(self.lines)):
            line = self.lines[i]
            if not line:
                continue
            if isinstance(line, BMComment):
                table += line.toTable()
            else:
                table += line.toTable(linenumber)
                linenumber += 1
        table += "</table></body></html>"
        return table
