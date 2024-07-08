from typing import List

import bmgen.targets.bm as target
import bmgen.targets.bm.channel as channel
import bmgen.targets.bm.helper.cast as cast
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.battery import battery
from bmgen.targets.bm.stepinfo import BMStepInfo
from bmgen.targets.bm.time import time as _time


@cast.autocast()
def charge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] | None = None,
    registrations: List[BMRegistration] | None = None,
) -> BMStepInfo:
    if not limits:
        limits = []
    if not (
        isinstance(current, BMMultiplication)
        and current.channel.name == battery.oneC.name
    ):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, BMVariable("V")))

    return target.generator.add(
        BMStatement(
            operator="CHA", values=values, limits=limits, registrations=registrations
        )
    )


@cast.autocast()
def discharge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] | None = None,
    registrations: List[BMRegistration] | None = None,
) -> BMStepInfo:
    if not limits:
        limits = []
    if not (
        isinstance(current, BMMultiplication)
        and current.channel.name == battery.oneC.name
    ):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, BMVariable("V")))

    return target.generator.add(
        BMStatement(
            operator="DCH", values=values, limits=limits, registrations=registrations
        )
    )


@cast.autocast()
def pause(
    limits: List[BMLimit] | None = None,
    hours: BMNumValue | None = None,
    minutes: BMNumValue | None = None,
    seconds: BMNumValue | None = None,
    registrations: List[BMRegistration] | None = None,
) -> BMStepInfo:
    if not limits:
        limits = []
    if hours or minutes or seconds:
        limits.append(time(hours, minutes, seconds).toLimit())
    return target.generator.add(
        BMStatement(operator="PAU", limits=limits, registrations=registrations)
    )


def limit(condition: BMLimitCondition, action: BMAction | None = None):
    if isinstance(condition, _time):
        condition = BMLimitTime(condition.toBMTime())
    return BMLimit(condition=condition, action=action)


def limit_global(condition: BMLimitCondition, action: BMAction | None = None):
    if isinstance(condition, _time):
        condition = BMLimitTime(condition.toBMTime())
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


@cast.autocast()
def seconds(value: BMNumValue) -> _time:
    return _time(None, None, value)


@cast.autocast()
def minutes(value: BMNumValue) -> _time:
    pass
    return _time(None, value, None)


@cast.autocast()
def hours(value: BMNumValue) -> _time:
    return _time(value, None, None)


def error(errnum: int):
    return BMError(errnum)


def register_global(
    time: _time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    regs = register(time, voltage, current, format)
    target.generator.add(BMStatement(operator="SET", registrations=regs))


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
    return regs
