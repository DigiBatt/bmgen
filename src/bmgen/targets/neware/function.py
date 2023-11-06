import bmgen.targets.neware as target
from bmgen.targets.neware.ast import *
from bmgen.targets.neware.constants import StepType, LimitType, NewareAction, RecordType
from bmgen.targets.neware.helper.cast import limitcast
from typing import List


def charge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit | NewareExpression] | None = None,
    registrations: Dict[RecordType, float] | None = None,
):
    limits = limitcast(limits)
    if voltage:
        args, protections = _limits_to_args(
            limits,
            {
                LimitType.CurrentLower: "cutoffCurrent",
                LimitType.CapacityUpper: "capacity",
                LimitType.Time: "steptime",
            },
        )
        if not "cutoffCurrent" in args:
            raise NotImplementedError(
                "CCCV charge step must have a current cutoff condition"
            )
        return target.generator.add(
            NewareStatement(
                operator=StepType.CCCV_Chg,
                current=current,
                voltage=voltage,
                record=registrations,
                **args
            )
        )
    else:
        args, protections = _limits_to_args(
            limits,
            {
                LimitType.VoltageUpper: "cutoffVoltage",
                LimitType.CapacityUpper: "capacity",
                LimitType.Time: "steptime",
            },
        )
        if not "cutoffVoltage" in args:
            raise NotImplementedError(
                "CC charge step must have a voltage cutoff condition"
            )
        return target.generator.add(
            NewareStatement(
                operator=StepType.CC_Chg, current=current, record=registrations, **args
            )
        )


def discharge(
    current: float,
    voltage: float | None = None,
    limits: List[NewareLimit | NewareExpression] | None = None,
    registrations: Dict[RecordType, float] | None = None,
):
    limits = limitcast(limits)
    if voltage:
        args, protections = _limits_to_args(
            limits,
            {
                LimitType.CurrentLower: "cutoffCurrent",
                LimitType.CapacityUpper: "capacity",
                LimitType.Time: "steptime",
            },
        )
        if not "cutoffCurrent" in args:
            raise NotImplementedError(
                "CCCV discharge step must have a current cutoff condition"
            )
        return target.generator.add(
            NewareStatement(
                operator=StepType.CCCV_DChg,
                current=current,
                voltage=voltage,
                record=registrations,
                **args
            )
        )
    else:
        args, protections = _limits_to_args(
            limits,
            {
                LimitType.VoltageLower: "cutoffVoltage",
                LimitType.CapacityUpper: "capacity",
                LimitType.Time: "steptime",
            },
        )
        if not "cutoffVoltage" in args:
            raise NotImplementedError(
                "CC discharge step must have a voltage cutoff condition"
            )
        return target.generator.add(
            NewareStatement(
                operator=StepType.CC_DChg, current=current, record=registrations, **args
            )
        )


def pause(
    limits: List[NewareLimit | NewareExpression] | None = None,
    hours: float = 0,
    minutes: float = 0,
    seconds: float = 0,
    registrations: Dict[RecordType, float] | None = None,
):
    limits = limitcast(limits)
    if hours or minutes or seconds:
        limits.append(time(hours, minutes, seconds).toLimit())
    args, protections = _limits_to_args(limits, {LimitType.Time: "steptime"})
    return target.generator.add(
        NewareStatement(operator=StepType.Rest, record=registrations, **args)
    )


@dataclass
class time:
    hours: float = 0
    minutes: float = 0
    seconds: float = 0

    def toNumber(self) -> float:
        return self.seconds + (self.minutes + self.hours * 60) * 60

    def toLimit(self) -> NewareLimit:
        return NewareLimit(LimitType.Time, self.toNumber())


def seconds(value: float) -> time:
    return time(0, 0, value)


def minutes(value: float) -> time:
    return time(0, value, 0)


def hours(value: float) -> time:
    return time(value, 0, 0)


def _limits_to_args(limits: List[NewareLimit], limitArgs: Dict[LimitType, str]):
    args = {}
    protections = []
    for l in limits:
        if isinstance(l, NewareExpression):
            if not "others" in args:
                args["others"] = []
            args["others"].append(l)
        else:
            if l.type in limitArgs and l.action == NewareAction.NextStep:
                args[limitArgs[l.type]] = l.value
            else:
                protections.append(l)
    return (args, protections)


def limit(condition: NewareLimit, action: NewareAction = NewareAction.NextStep):
    condition.action = action
    return condition


def limit_global(condition: NewareLimit, action: NewareAction = NewareAction.NextStep):
    target.generator.program.protections[condition.type] = condition.value


def error(errnum: int):
    return NewareAction.Protected


def register_global(
    time: time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    record = register(time, voltage, current, format)
    target.generator.program.record = record


def register(
    time: time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
) -> Dict[RecordType, float]:
    record = {}
    if time:
        record[RecordType.Time] = time.toNumber()
    if voltage:
        record[RecordType.Voltage] = voltage
    if current:
        record[RecordType.Current] = current
    return record
