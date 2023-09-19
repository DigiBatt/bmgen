import bmgen.targets.bm as target
from bmgen.targets.bm.ast import *
import bmgen.targets.bm.helper.cast as cast
from typing import List
from bmgen.targets.bm.battery import battery
import bmgen.targets.bm.channel as channel
from bmgen.targets.bm.time import time as _time


@cast.autocast()
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


@cast.autocast()
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


@cast.autocast()
def pause(
    limits: List[BMLimit] | None = None,
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
):
    if not limits:
        limits = []
    if hours or minutes or seconds:
        limits.append(time(hours, minutes, seconds).toLimit())
    target.generator.add(BMStatement(operator="PAU", limits=limits))


def limit(condition: BMLimitCondition, action: BMAction | None = None):
    return BMLimit(condition=condition, action=action)


def limit_global(condition: BMLimitCondition, action: BMAction | None = None):
    target.generator.add(
        BMStatement(
            operator="SET", limits=[BMLimit(condition=condition, action=action)]
        )
    )


@cast.autocast()
def time(
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
) -> _time:
    return _time(hours, minutes, seconds)


def error(errnum: int):
    return BMError(errnum)


def register(
    time: _time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    regs = []
    if format:
        for f in format:
            regs.append(BMRegFormat(f))
    if time:
        t = time.toBMTime()
        regs.append(BMRegCondition(value=t.value, channel=BMVariable(t.unit)))
    if voltage:
        regs.append(BMRegCondition(value=BMNumber(voltage), channel=channel.V))
    if current:
        regs.append(BMRegCondition(value=BMNumber(current), channel=channel.I))
    target.generator.add(BMStatement(operator="SET", registrations=regs))
