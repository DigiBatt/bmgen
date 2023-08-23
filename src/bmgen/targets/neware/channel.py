from bmgen.targets.neware.ast import NewareLimit
from bmgen.targets.neware.constants import LimitType


class NewareCurrent:
    def __lt__(self, other: float):
        return NewareLimit(LimitType.CurrentLower, other)

    def __gt__(self, other: float):
        return NewareLimit(LimitType.CurrentUpper, other)


class NewareVoltage:
    def __lt__(self, other: float):
        return NewareLimit(LimitType.VoltageLower, other)

    def __gt__(self, other: float):
        return NewareLimit(LimitType.VoltageUpper, other)


I = NewareCurrent()
V = NewareVoltage()
