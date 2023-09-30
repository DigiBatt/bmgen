import bmgen.targets.basytec as target
from bmgen.targets.basytec.ast import *
from bmgen.targets.basytec.constants import StepType
from bmgen.targets.basytec.helper.cast import autocast, limitcast
from bmgen.targets.basytec.channel import I, V, t
from typing import List


@autocast(current="A", voltage="V")
def charge(
    current: BasytecValueLiteral,
    voltage: BasytecValueLiteral | None = None,
    limits: List[BasytecLimit] | None = None,
):
    limits = limitcast(limits)
    params = [BasytecSetValue(I, current)]
    if voltage:
        params.append(BasytecSetValue(V, voltage))
    return target.generator.add(
        BasytecStatement(operator=StepType.Charge, parameters=params, limits=limits)
    )


@autocast(current="A", voltage="V")
def discharge(
    current: BasytecValueLiteral,
    voltage: BasytecValueLiteral | None = None,
    limits: List[BasytecLimit] | None = None,
):
    limits = limitcast(limits)
    params = [BasytecSetValue(I, current)]
    if voltage:
        params.append(BasytecSetValue(V, voltage))
    return target.generator.add(
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
    return target.generator.add(
        BasytecStatement(operator=StepType.Pause, limits=limits)
    )


@dataclass
class time:
    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None

    def toValue(self) -> BasytecValueLiteral:
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
        return BasytecValueLiteral(value=value, unit=unit)

    def toLimit(self) -> BasytecLimit:
        return BasytecLimit(channel=t, operator=">", value=self.toValue())


def seconds(value: float) -> time:
    return time(None, None, value)


def minutes(value: float) -> time:
    return time(None, value, None)


def hours(value: float) -> time:
    return time(value, None, None)


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


@autocast(current="A", voltage="V")
def register(
    time: time | None = None,
    voltage: BasytecValueLiteral | None = None,
    current: BasytecValueLiteral | None = None,
    format: List | None = None,
):
    regs = []
    if time:
        regs.append(BasytecSetValue(channel=t, value=time.toValue()))
    if voltage:
        regs.append(BasytecSetValue(channel=V, value=voltage))
    if current:
        regs.append(BasytecSetValue(channel=I, value=current))
    target.generator.set_registration(regs)
