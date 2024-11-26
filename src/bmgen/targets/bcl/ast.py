from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List

from bmgen.targets.bcl.constants import TERMINATION_UNITS
from bmgen.targets.bm.helper.compare import compare


@dataclass
class BCLUnit:
    name: str

    def toDict(self):
        return self.name


@dataclass
class BCLValue(ABC):
    unit: BCLUnit


@dataclass
class BCLParameter(BCLValue):
    name: str
    value: float

    def toDict(self):
        return self.name


@dataclass
class BCLValueLiteral(BCLValue):
    value: float

    def toDict(self):
        return self.value


@dataclass
class BCLStepType:
    name: str

    def toDict(self):
        return self.name


@compare
@dataclass
class BCLTerminationType:
    name: str

    def toDict(self):
        return self.name

    def __compare__(self, other, operator):
        if not isinstance(other, BCLValue):
            other = BCLValueLiteral(BCLUnit(TERMINATION_UNITS[self.name]), other)
        return BCLTermination(self, other)


@dataclass
class BCLTermination:
    type: BCLTerminationType
    value: BCLValue

    def toDict(self):
        return {
            "type": self.type.toDict(),
            "value": self.value.toDict(),
            "unit": self.value.unit.toDict(),
        }


@dataclass
class BCLStep:
    type: BCLStepType
    value: BCLValue
    terminations: List[BCLTermination] | None

    def toDict(self):
        return {
            "type": self.type.toDict(),
            "value": self.value.toDict(),
            "unit": self.value.unit.toDict(),
            "termination": (
                [t.toDict() for t in self.terminations] if self.terminations else []
            ),
        }


@dataclass
class BCLInstruction:
    sequence: List[BCLStep]
    repetitions: int

    def toDict(self):
        return {
            "sequence": [step.toDict() for step in self.sequence],
            "repeat": self.repetitions,
        }


@dataclass
class BCLProgram:
    name: str
    parameters: Dict[str, float]
    instructions: List[BCLInstruction]

    def toDict(self):
        return {
            "name": self.name,
            "parameters": self.parameters,
            "instructions": [i.toDict() for i in self.instructions],
        }
