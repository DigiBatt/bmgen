from bmgen.targets.basytec import generator
from bmgen.targets.basytec.ast import *
from bmgen.targets.basytec.constants import StepType
from bmgen.targets.basytec.helper.cast import autocast
from bmgen.targets.basytec.channel import I, V, t
from typing import List


@autocast(current="A", voltage="V")
def charge(
    current: BasytecValue,
    voltage: BasytecValue | None = None,
    limits: List[BasytecLimit] = [],
):
    params = [BasytecParameter(I, current)]
    if voltage:
        params.append(BasytecParameter(V, voltage))
    generator.add(
        BasytecStatement(operator=StepType.Charge, parameters=params, limits=limits)
    )


@autocast(current="A", voltage="V")
def discharge(
    current: BasytecValue,
    voltage: BasytecValue | None = None,
    limits: List[BasytecLimit] = [],
):
    params = [BasytecParameter(I, current)]
    if voltage:
        params.append(BasytecParameter(V, voltage))
    generator.add(
        BasytecStatement(operator=StepType.Discharge, parameters=params, limits=limits)
    )


def pause(limits: List[BasytecLimit]):
    generator.add(BasytecStatement(operator=StepType.Pause, limits=limits))


def time(
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
) -> BasytecLimit:
    if hours:
        if minutes or seconds:
            raise NotImplementedError("Basytec time limit can only have one unit")
        value = hours
        unit = BasytecUnit("h")
    if minutes:
        if hours or seconds:
            raise NotImplementedError("Basytec time limit can only have one unit")
        value = minutes
        unit = BasytecUnit("min")
    if seconds:
        if hours or minutes:
            raise NotImplementedError("Basytec time limit can only have one unit")
        value = seconds
        unit = BasytecUnit("s")
    return BasytecLimit(
        channel=t, operator=">", value=BasytecValue(value=value, unit=unit)
    )


def limit(condition: BasytecLimit, action: BasytecAction | None = None):
    condition.action = action
    return condition


def limit_global(condition: BasytecLimit, action: BasytecAction | None = None):
    condition.action = None
    generator.program.limits.append(condition)
    return condition


def error(errnum: int):
    generator.stoplabel = True
    return BasytecGoto("STOP")
