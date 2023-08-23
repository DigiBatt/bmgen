from bmgen.targets.neware import generator
from bmgen.targets.neware.ast import *
from bmgen.targets.neware.constants import StepType, LimitType, LimitArgs
from typing import List


def charge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit] = [],
):
    args, protections = _limits_to_args(limits)
    if voltage:
        generator.add(
            NewareStatement(
                operator=StepType.CCCV_Chg, current=current, voltage=voltage, *args
            )
        )
    else:
        generator.add(NewareStatement(operator=StepType.CC_Chg, current=current, *args))


def discharge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit] = [],
):
    args, protections = _limits_to_args(limits)
    if voltage:
        generator.add(
            NewareStatement(
                operator=StepType.CCCV_DChg, current=current, voltage=voltage, *args
            )
        )
    else:
        generator.add(
            NewareStatement(operator=StepType.CC_DChg, current=current, *args)
        )


def pause(
    limits: Dict[LimitType, float] = {},
):
    args, protections = _limits_to_args(limits)
    generator.add(NewareStatement(operator=StepType.Rest, *args))


def time(
    hours: float = 0,
    minutes: float = 0,
    seconds: float = 0,
) -> float:
    return seconds + (minutes + hours * 60) * 60


def _limits_to_args(limits: List[NewareLimit]):
    args = {}
    protections = []
    for l in limits:
        if l.protection:
            protections.append(l)
        else:
            args[LimitArgs[l.type]] = l.value
    return (args, protections)


# def limit(condition: BMLimitCondition, action: BMAction | None = None):
#     return NewareLimit()


# def limit_global(condition: BMLimitCondition, action: BMAction | None = None):
#     generator.add(
#         BMStatement(
#             operator="SET", limits=[BMLimit(condition=condition, action=action)]
#         )
#     )


# def error(errnum: int):
#     return BMError(errnum)
