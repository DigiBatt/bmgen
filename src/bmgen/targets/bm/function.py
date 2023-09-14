import bmgen.targets.bm as target
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.helper.cast import autocast
from typing import List
from bmgen.targets.bm.battery import battery


@autocast()
def charge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] | None = None,
):
    if not limits:
        limits = []
    if not (
        isinstance(current, BMMultiplication)
        and current.variable.name == battery.oneC.name
    ):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, BMVariable("V")))

    target.generator.add(BMStatement(operator="CHA", values=values, limits=limits))


@autocast()
def discharge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] | None = None,
):
    if not limits:
        limits = []
    if not (
        isinstance(current, BMMultiplication)
        and current.variable.name == battery.oneC.name
    ):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, BMVariable("V")))

    target.generator.add(BMStatement(operator="DCH", values=values, limits=limits))


@autocast()
def time(
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
) -> BMLimitCondition:
    if seconds:
        if hours:
            if isinstance(hours, BMNumber) and isinstance(seconds, BMNumber):
                seconds.value += hours.value * 3600
            else:
                raise NotImplementedError("BM time limit can only have one unit")
        if minutes:
            if isinstance(minutes, BMNumber) and isinstance(seconds, BMNumber):
                seconds.value += minutes.value * 60
            else:
                raise NotImplementedError("BM time limit can only have one unit")
        return BMLimitTime(value=seconds, unit="s")
    if minutes:
        if hours:
            if isinstance(hours, BMNumber) and isinstance(minutes, BMNumber):
                minutes.value += hours.value * 60
            else:
                raise NotImplementedError("BM time limit can only have one unit")
        return BMLimitTime(value=minutes, unit="min")
    if hours:
        return BMLimitTime(value=hours, unit="h")


@autocast()
def pause(
    limits: List[BMLimit] | None = None,
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
):
    if not limits:
        limits = []
    if hours or minutes or seconds:
        limits.append(BMLimit(time(hours, minutes, seconds)))
    target.generator.add(BMStatement(operator="PAU", limits=limits))


def limit(condition: BMLimitCondition, action: BMAction | None = None):
    return BMLimit(condition=condition, action=action)


def limit_global(condition: BMLimitCondition, action: BMAction | None = None):
    target.generator.add(
        BMStatement(
            operator="SET", limits=[BMLimit(condition=condition, action=action)]
        )
    )


def error(errnum: int):
    return BMError(errnum)
