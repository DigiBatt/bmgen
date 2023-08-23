from bmgen.targets.bm import generator
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.helper.cast import autocast
from typing import List


@autocast()
def charge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] = [],
):
    if isinstance(current, BMNumValue):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, "V"))

    generator.add(BMStatement(operator="CHA", values=[current], limits=limits))


@autocast()
def discharge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] = [],
):
    if isinstance(current, BMNumValue):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, "V"))

    generator.add(BMStatement(operator="DCH", values=[current], limits=limits))


@autocast()
def time(
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
) -> BMLimitCondition:
    if hours:
        if minutes or seconds:
            raise NotImplementedError("BM time limit can only have one unit")
        return BMLimitTime(value=hours, unit="h")
    if minutes:
        if hours or seconds:
            raise NotImplementedError("BM time limit can only have one unit")
        return BMLimitTime(value=hours, unit="min")
    if seconds:
        if hours or minutes:
            raise NotImplementedError("BM time limit can only have one unit")
        return BMLimitTime(value=hours, unit="s")


@autocast()
def pause(
    limits: List[BMLimit] = [],
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
):
    if hours or minutes or seconds:
        limits.append(BMLimit(time(hours, minutes, seconds)))
    generator.add(BMStatement(operator="PAU", limits=limits))


def limit(condition: BMLimitCondition, action: BMAction | None = None):
    return BMLimit(condition=condition, action=action)


def limit_global(condition: BMLimitCondition, action: BMAction | None = None):
    generator.add(
        BMStatement(
            operator="SET", limits=[BMLimit(condition=condition, action=action)]
        )
    )


def error(errnum: int):
    return BMError(errnum)
