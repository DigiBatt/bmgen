from dataclasses import dataclass
from typing import Any, List

import bmgen.targets.bcl as target
from bmgen.targets.bcl.ast import (
    BCLStep,
    BCLStepType,
    BCLTermination,
    BCLUnit,
    BCLValue,
    BCLValueLiteral,
)
from bmgen.targets.bcl.channel import I, V, t
from bmgen.targets.bcl.helper.cast import autocast


@autocast(current="Ampere", voltage="Volt")
def charge(
    current: BCLValue,
    voltage: BCLValue | None = None,
    limits: List[BCLTermination] | None = None,
    registrations: Any = None,
):
    if isinstance(current, BCLValueLiteral):
        current.value *= -1
    ccStep = target.generator.add(
        BCLStep(BCLStepType("ElectricCurrent"), current, limits)
    )
    if voltage is not None:
        target.generator.add(BCLStep(BCLStepType("Voltage"), voltage, limits))
    return ccStep


@autocast(current="Ampere", voltage="Volt")
def discharge(
    current: BCLValue,
    voltage: BCLValue | None = None,
    limits: List[BCLTermination] | None = None,
    registrations: Any = None,
):
    ccStep = target.generator.add(
        BCLStep(BCLStepType("ElectricCurrent"), current, limits)
    )
    if voltage is not None:
        target.generator.add(BCLStep(BCLStepType("Voltage"), voltage, limits))
    return ccStep


def pause(
    limits: List[BCLTermination] | None = None,
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
    registrations: Any = None,
):
    return target.generator.add(
        BCLStep(BCLStepType("Rest"), time(hours, minutes, seconds).toValue(), limits)
    )


@dataclass
class time:
    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None

    def toValue(self) -> BCLValueLiteral:
        value = 0.0
        if self.seconds is not None:
            value = self.seconds
        if self.minutes is not None:
            value += self.minutes * 60
        if self.hours is not None:
            value += self.hours * 3600
        return BCLValueLiteral(value=value, unit=BCLUnit("Second"))

    def toLimit(self) -> BCLTermination:
        return BCLTermination(t, value=self.toValue())


def seconds(value: float) -> time:
    return time(None, None, value)


def minutes(value: float) -> time:
    return time(None, value, None)


def hours(value: float) -> time:
    return time(value, None, None)


def limit(condition: BCLTermination, action: Any | None = None):
    # if action is not None:
    #     raise Exception("Limit actions not supported for BCL")
    return condition


def limit_global(condition: BCLTermination, action: Any | None = None):
    # raise Exception("Global limits not supported for BCL")
    return None


def error(errnum: int):
    # raise Exception("Errors not supported for BCL")
    return None


def register_global(
    time: time | None = None,
    voltage: BCLValue | None = None,
    current: BCLValue | None = None,
    format: List | None = None,
):
    pass


def register(
    time: time | None = None,
    voltage: BCLValue | None = None,
    current: BCLValue | None = None,
    format: List | None = None,
):
    pass
