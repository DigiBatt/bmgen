import itertools
import typing
from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List

import bmgen.targets.jsonld.constants as constants
from bmgen.targets.bm.helper.compare import compare
import bmgen.targets.jsonld.ontology as ontology


@dataclass
class BCLUnit:
    name: str

    def toDict(self):
        return self.name

    def __rmul__(self, other):
        if not isinstance(other, float):
            return NotImplemented
        return BCLValueLiteral(self, other)


@dataclass
class BCLValue(ABC):
    unit: BCLUnit


@dataclass
class BCLParameter(BCLValue):
    name: str
    value: float

    def toDict(self):
        return self.name

    def __mul__(self, other):
        if not isinstance(other, BCLUnit):
            return NotImplemented
        return BCLParameter(other, self.name, self.value)


@dataclass
class BCLValueLiteral(BCLValue):
    value: float

    def toDict(self):
        return self.value

    def __mul__(self, other):
        if not isinstance(other, BCLUnit):
            return NotImplemented
        return BCLValueLiteral(other, self.value)


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
        if hasattr(other, "seconds"):
            return other.toLimit()
        if not isinstance(other, BCLValue):
            other = BCLValueLiteral(
                BCLUnit(constants.TERMINATION_UNITS[self.name]), other
            )
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


@dataclass
class NumericValue:
    pass


@compare
@dataclass
class Channel(NumericValue):
    quantity: typing.Type[ontology.ElectrochemicalQuantity]
    unit: ontology.MeasurementUnit

    def toOntology(self):
        return (self.quantity, self.unit.__name__)

    def __compare__(self, other, operator):
        if isinstance(other, (float, int)):
            other = NumericLiteral(other, self.unit)
        quantity = self.quantity
        if self.quantity in constants.LOWER_LIMITS and operator in ["<", "<="]:
            quantity = constants.LOWER_LIMITS[self.quantity]
        elif self.quantity in constants.UPPER_LIMITS and operator in [">", ">="]:
            quantity = constants.UPPER_LIMITS[self.quantity]
        return Limit(quantity, other)


@dataclass
class NumericLiteral(NumericValue):
    value: float
    unit: ontology.MeasurementUnit

    def toOntology(self):
        return (self.value, self.unit.__name__)

    def __mul__(self, other: float | int):
        if not isinstance(other, (float, int)):
            return NotImplemented
        return NumericLiteral(self.value * other, self.unit)

    def __rmul__(self, other: float):
        return self.__mul__(other)


@dataclass
class Setpoint:
    type: typing.Type[ontology.ElectrochemicalQuantity]
    value: NumericValue

    def toOntology(self):
        return create_property(self.type, self.value)


@dataclass
class Limit:
    type: typing.Type[ontology.ElectrochemicalQuantity]
    value: NumericValue

    def toOntology(self):
        return create_property(self.type, self.value)


@dataclass
class Step:
    instance: ontology.Procedure
    setpoints: List[Setpoint]
    limits: List[Limit]

    def toOntology(self):
        self.instance.hasProcessParameter = [
            item.toOntology() for item in itertools.chain(self.setpoints, self.limits)
        ]
        return self.instance


@dataclass
class Program:
    steps: List[Step]

    def toOntology(self):
        test = ontology.BatteryTest()
        tasks = [s.toOntology() for s in self.steps]
        # test.hasTask = tasks
        if len(tasks) > 0:
            # test.hasBeginTask = tasks[0]
            test.hasTask = tasks[0]
            for i in range(len(tasks) - 1):
                tasks[i].hasNext = tasks[i + 1]
        return test


@dataclass
class Reference:
    id: str


def create_property(
    type: typing.Type[ontology.ElectrochemicalQuantity], value: NumericValue | Reference
):
    if issubclass(type, ontology.Voltage):
        unitName = "Volt"
    elif issubclass(type, ontology.ElectricCurrent):
        unitName = "Ampere"
    elif issubclass(type, ontology.ElectricCharge):
        unitName = "Coulomb"
    elif issubclass(type, ontology.ElectricResistance):
        unitName = "Ohm"
    elif issubclass(type, ontology.EnergyDensity):
        unitName = "NewtonPerSquareCentiMetre"
    else:
        # raise Exception(f"Cannot determine unit for type {type.__name__}")
        unitName = "Volt"
    if isinstance(value, NumericLiteral) and isinstance(value.value, Reference):
        prop = type(None, None)
        prop.identifier = value.value.id
    elif isinstance(value, NumericValue):
        if type == ontology.ChargingCurrent and issubclass(
            value.unit, ontology.CRateUnit
        ):
            type = ontology.ChargingCRate
        if type == ontology.DischargingCurrent and issubclass(
            value.unit, ontology.CRateUnit
        ):
            type = ontology.DischargingCRate
        prop = type(*value.toOntology())
    elif isinstance(value, Reference):
        prop = type(None, None)
        prop.identifier = value.id
    return prop


@compare
@dataclass
class UnsupportedChannel(NumericValue):

    message: str

    def toOntology(self):
        raise Exception(self.message)
