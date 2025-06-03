from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

from bmgen.targets.bcl.constants import TERMINATION_UNITS
from bmgen.targets.bm.helper.compare import compare


class Statement(ABC):
    @abstractmethod
    def toText(self) -> str:
        pass


class Expression(Statement, ABC):
    pass


@dataclass
class FunctionCall(Expression):
    function: str
    args: List[Expression] = field(default_factory=list)
    kwargs: Dict[str, Expression] = field(default_factory=dict)

    def toText(self) -> str:
        argitems = [v.toText() for v in self.args]
        argitems += [f"{k}={v.toText()}" for k, v in self.kwargs.items()]
        argstring = ", ".join(argitems)
        return f"{self.function}({argstring})"


@dataclass
class Import:
    module: str
    symbols: List[str] | None = None
    alias: str | None = None

    def toText(self) -> str:
        if self.symbols is None:
            s = f"import {self.module}"
        else:
            s = f"from {self.module} import " + ", ".join(self.symbols)
        if self.alias is not None:
            s += f" as {self.alias}"
        return s


@dataclass
class NumberLiteral(Expression):
    value: float

    def toText(self) -> str:
        return str(self.value)


@dataclass
class Variable(Expression):
    name: str

    def toText(self) -> str:
        return self.name


@dataclass
class BinaryOperation(Expression):
    operator: str
    left: Expression
    right: Expression

    def toText(self) -> str:
        return f"{self.left.toText()} {self.operator} {self.right.toText()}"


@dataclass
class ListLiteral(Expression):
    items: List[Expression]

    def toText(self) -> str:
        return "[" + ", ".join([i.toText() for i in self.items]) + "]"


@dataclass
class Program:
    statements: List[Statement] = field(default_factory=list)

    def toText(self) -> str:
        return "\n".join([s.toText() for s in self.statements])
