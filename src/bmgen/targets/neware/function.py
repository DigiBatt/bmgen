from bmgen.targets.neware import generator
from bmgen.targets.neware.ast import *
from bmgen.targets.neware.constants import StepType, LimitType, LimitArgs, NewareAction
from typing import List


def charge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit] = [],
):
    args, protections = _limits_to_args(limits)
    if voltage:
        if not "cutoffCurrent" in args:
            raise NotImplementedError(
                "CC charge step must have a current cutoff condition"
            )
        generator.add(
            NewareStatement(
                operator=StepType.CCCV_Chg, current=current, voltage=voltage, **args
            )
        )
    else:
        if not "cutoffVoltage" in args:
            raise NotImplementedError(
                "CCCV charge step must have a voltage cutoff condition"
            )
        generator.add(
            NewareStatement(operator=StepType.CC_Chg, current=current, **args)
        )


def discharge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit] = [],
):
    args, protections = _limits_to_args(limits)
    if voltage:
        if not "cutoffCurrent" in args:
            raise NotImplementedError(
                "CC discharge step must have a current cutoff condition"
            )
        generator.add(
            NewareStatement(
                operator=StepType.CCCV_DChg, current=current, voltage=voltage, **args
            )
        )
    else:
        if not "cutoffVoltage" in args:
            raise NotImplementedError(
                "CCCV discharge step must have a voltage cutoff condition"
            )
        generator.add(
            NewareStatement(operator=StepType.CC_DChg, current=current, **args)
        )


def pause(
    limits: Dict[LimitType, float] = {},
):
    args, protections = _limits_to_args(limits)
    generator.add(NewareStatement(operator=StepType.Rest, **args))


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
        if l.type in LimitArgs and l.action == NewareAction.NextStep:
            args[LimitArgs[l.type]] = l.value
        else:
            protections.append(l)
    return (args, protections)


def limit(condition: NewareLimit, action: NewareAction = NewareAction.NextStep):
    condition.action = action
    return condition


def limit_global(condition: NewareLimit, action: NewareAction = NewareAction.NextStep):
    generator.program.protections[condition.type] = condition.value


def error(errnum: int):
    return NewareAction.Protected
