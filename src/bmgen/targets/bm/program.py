from bmgen.targets.bm.ast import (
    BMVariable,
    BMStatement,
    BMAssignment,
    BMNumber,
    BMLimit,
    BMLimitCondition,
    BMAction,
)
from bmgen.targets.bm import generator


def variable(name: str, value: float | None = None):
    var = BMVariable(name)
    if value:
        generator.add(
            BMStatement(
                operator="SET",
                values=[BMAssignment(variable=var, numvalue=BMNumber(value))],
            )
        )
    return var


def limit(condition: BMLimitCondition, action: BMAction):
    return BMLimit(condition=condition, action=action)
