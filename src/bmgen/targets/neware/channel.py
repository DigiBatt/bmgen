from bmgen.targets.neware.ast import (
    NewareLimit,
    NewareExpression,
    NewareExpressionString,
)
from bmgen.targets.neware.constants import (
    LimitType,
    NewareComparator,
    ExpressionVariableId,
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
            )
        else:
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + str(other)),
                NewareComparator.Less,
            )

    def __gt__(self, other: float | NewareExpressionString):
        if isinstance(other, NewareExpressionString):
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + other.expression),
                NewareComparator.Greater,
            )
        else:
            return NewareExpression(
                ExpressionVariableId,
                ExpressionVariableId,
                "expr1",
                NewareExpressionString("Ah - " + str(other)),
                NewareComparator.Greater,
            )


I = NewareCurrent()
V = NewareVoltage()
StepCharge = NewareStepCharge()
