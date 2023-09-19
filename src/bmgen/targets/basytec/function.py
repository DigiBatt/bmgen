import bmgen.targets.basytec as target
from bmgen.targets.basytec.ast import *
from bmgen.targets.basytec.constants import StepType
from bmgen.targets.basytec.helper.cast import autocast, limitcast
from bmgen.targets.basytec.channel import I, V, t
from typing import List


@autocast(current="A", voltage="V")
def charge(
    current: BasytecValue,
    voltage: BasytecValue | None = None,
    limits: List[BasytecLimit] | None = None,
):
    limits = limitcast(limits)
    params = [BasytecParameter(I, current)]
    if voltage:
        params.append(BasytecParameter(V, voltage))
    target.generator.add(
        BasytecStatement(operator=StepType.Charge, parameters=params, limits=limits)
    )


@autocast(current="A", voltage="V")
def discharge(
    current: BasytecValue,
    voltage: BasytecValue | None = None,
    limits: List[BasytecLimit] | None = None,
):
    limits = limitcast(limits)
    params = [BasytecParameter(I, current)]
    if voltage:
        params.append(BasytecParameter(V, voltage))
    target.generator.add(
        BasytecStatement(operator=StepType.Discharge, parameters=params, limits=limits)
    )


def pause(
    limits: List[BasytecLimit] | None = None,
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
):
    limits = limitcast(limits)
    if hours or minutes or seconds:
        limits.append(time(hours, minutes, seconds).toLimit())
    target.generator.add(BasytecStatement(operator=StepType.Pause, limits=limits))


@dataclass
class time:
    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None

    def toLimit(self) -> BasytecLimit:
        if self.seconds:
            value = self.seconds
            unit = BasytecUnit("s")
            if self.hours:
                value += self.hours * 3600
            if self.minutes:
                value += self.minutes * 60
        elif self.minutes:
            value = self.minutes
            unit = BasytecUnit("min")
            if self.hours:
                value += self.hours * 60
        elif self.hours:
            value = self.hours
            unit = BasytecUnit("h")
        return BasytecLimit(
            channel=t, operator=">", value=BasytecValue(value=value, unit=unit)
        )


def limit(condition: BasytecLimit, action: BasytecAction | None = None):
    condition.action = action
    return condition


def limit_global(condition: BasytecLimit, action: BasytecAction | None = None):
    condition.action = None
    target.generator.program.limits.append(condition)
    return condition


def error(errnum: int):
    target.generator.stoplabel = True
    return BasytecGoto("STOP")
