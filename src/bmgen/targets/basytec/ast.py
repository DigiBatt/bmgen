from bmgen.targets.basytec.constants import StepType, Newline
from dataclasses import dataclass, field
from typing import List
from abc import ABC


@dataclass
class BasytecUnit:
    name: str


@dataclass
class BasytecChannel:
    name: str
    unit: BasytecUnit

    def __lt__(self, other):
        if isinstance(other, BasytecValue):
            value = other
        else:
            value = BasytecValueLiteral(other, self.unit)
        return BasytecLimit(self, "<", value)

    def __le__(self, other):
        if isinstance(other, BasytecValue):
            value = other
        else:
            value = BasytecValueLiteral(other, self.unit)
        return BasytecLimit(self, "<=", value)

    def __gt__(self, other):
        if isinstance(other, BasytecValue):
            value = other
        else:
            value = BasytecValueLiteral(other, self.unit)
        return BasytecLimit(self, ">", value)

    def __ge__(self, other):
        if isinstance(other, BasytecValue):
            value = other
        else:
            value = BasytecValueLiteral(other, self.unit)
        return BasytecLimit(self, ">=", value)


class BasytecAction:
    def toText(self):
        raise NotImplementedError()


class BasytecNext(BasytecAction):
    def toText(self):
        return "Next"


@dataclass
class BasytecGoto(BasytecAction):
    target: str
    pass

    def toText(self):
        return f"Goto {self.target}"


class BasytecValue(ABC):
    pass

    def __mul__(self, other):
        raise Exception("Mathematical operations are not yet supported for Basytec.")

    def __add__(self, other):
        raise Exception("Mathematical operations are not yet supported for Basytec.")

    def __sub__(self, other):
        raise Exception("Mathematical operations are not yet supported for Basytec.")

    def __div__(self, other):
        raise Exception("Mathematical operations are not yet supported for Basytec.")


@dataclass
class BasytecValueLiteral(BasytecValue):
    value: float
    unit: BasytecUnit

    def toText(self):
        return f"{self.value}{self.unit.name}"

    def __rmul__(self, other):
        return BasytecValueLiteral(self.value * other, self.unit)


@dataclass
class BasytecVariable(BasytecValue):
    name: str

    def toText(self):
        return f"{self.name}"


@dataclass
class BasytecLimit:
    channel: BasytecChannel
    operator: str
    value: BasytecValueLiteral
    action: BasytecAction | None = None

    def toText(self):
        return (
            f"{self.channel.name}{self.operator}{self.value.toText()}",
            self.action.toText() if self.action else None,
        )


class BasytecParameter(ABC):
    pass


@dataclass
class BasytecSetValue(BasytecParameter):
    channel: BasytecChannel
    value: BasytecValueLiteral

    def toText(self):
        return f"{self.channel.name}={self.value.toText()}"


@dataclass
class BasytecCalculation(BasytecParameter):
    variable: BasytecVariable
    calculation: str

    def toText(self):
        return f"{self.variable.name}={self.calculation}"


@dataclass
class BasytecStatement:
    operator: StepType
    parameters: List[BasytecParameter] = field(default_factory=list)
    limits: List[BasytecLimit] = field(default_factory=list)
    registrations: List[BasytecSetValue] = field(default_factory=list)
    label: str | None = None

    def toText(self, linenumber: int):
        text = f"0 {linenumber} {linenumber}\n"
        text += f"1 {linenumber}\n"
        text += f"2 {linenumber} {self._str(self.label)}\n"
        text += f"3 {linenumber} {str(self.operator).split('.')[1].replace('_', '-')}\n"
        text += (
            f"4 {linenumber} {Newline.join([p.toText() for p in self.parameters])}\n"
        )
        if self.limits:
            limit, action = zip(*[l.toText() for l in self.limits])
            limit = Newline.join(limit)
            action = Newline.join([a if a else "" for a in action]).rstrip(Newline)
        else:
            limit = ""
            action = ""
        text += f"5 {linenumber} {limit}\n"
        text += f"6 {linenumber} {action}\n"
        reg = Newline.join([r.toText() for r in self.registrations])
        text += f"7 {linenumber} {reg}\n"
        text += f"8 {linenumber}\n"
        return text

    def toTable(self, linenumber):
        table = f"<tr><td>{linenumber}</td>"
        table += f"<td></td>"
        table += f"<td>{self._str(self.label)}</td>"
        table += f"<td>{str(self.operator).split('.')[1].replace('_', '-')}</td>"
        table += f"<td>{'<br>'.join([p.toText() for p in self.parameters])}</td>"
        if self.limits:
            limit, action = zip(*[l.toText() for l in self.limits])
        else:
            limit = ""
            action = ""
        limit = "<br>".join(limit)
        action = "<br>".join([a if a else "" for a in action])
        table += f"<td>{limit}</td>"
        table += f"<td>{action}</td>"
        reg = "<br>".join([r.toText() for r in self.registrations])
        table += f"<td>{reg}</td>"
        table += f"<td></td></tr>"
        return table

    def _str(self, value):
        if value == None:
            return ""
        return str(value)


@dataclass
class BasytecProgram:
    lines: List[BasytecStatement] = field(default_factory=list)
    limits: List[BasytecLimit] = field(default_factory=list)
    registration_format: List[str] = field(default_factory=list)

    def toText(self):
        text = f"Main\n{len(self.registration_format)}\n"
        for format in self.registration_format:
            text += f"{format}\n"
        text += f" 9 {len(self.lines) + 1}\n"
        text += "0 0\n1 0 Level\n2 0 Label\n3 0 Command\n4 0 Parameter\n5 0 Termination\n6 0 Action\n7 0 Registration\n8 0 Comment\n"
        for i, line in enumerate(self.lines, 1):
            text += line.toText(i)
        return text

    def toTable(self):
        table = "<table>\n<tr><th></th><th>Level</th><th>Label</th><th>Command</th><th>Parameter</th><th>Termination</th><th>Action</th><th>Registration</th><th>Comment</th></tr>\n"
        for i, line in enumerate(self.lines, 1):
            table += line.toTable(i)
        table += "</table>"
        return table
