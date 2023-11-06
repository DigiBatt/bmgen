from bmgen.targets.neware.ast import (
    NewareLimit,
    NewareExpression,
    NewareExpressionString,
)
from bmgen.targets.neware.constants import (
    LimitType,
    NewareComparator,
    ExpressionVariableId,
    NewareGotoTarget,
)


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


class NewareStepCharge:
    def __lt__(self, other: float | NewareExpressionString):
        if isinstance(other, NewareExpressionString):
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + other.expression),
                NewareComparator.Less,
                NewareGotoTarget.Next,
            )
        else:
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + str(other)),
                NewareComparator.Less,
                NewareGotoTarget.Next,
            )

    def __gt__(self, other: float | NewareExpressionString):
        if isinstance(other, NewareExpressionString):
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + other.expression),
                NewareComparator.Greater,
                NewareGotoTarget.Next,
            )
        else:
            return NewareLimit(LimitType.CapacityUpper, other)


I = NewareCurrent()
V = NewareVoltage()
StepCharge = NewareStepCharge()
