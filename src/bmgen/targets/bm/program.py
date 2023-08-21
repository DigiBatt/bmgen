from bmgen.targets.bm.ast import (
    BMVariable,
    BMStatement,
    BMAssignment,
    BMLimit,
    BMLimitCondition,
    BMAction,
    BMNumValue,
)
from bmgen.targets.bm import generator
from bmgen.targets.bm.helper.cast import autocast


@autocast("value")
def variable(name: str, value: BMNumValue | None = None):
    var = BMVariable(name)
    if value:
        generator.add(
            BMStatement(
                operator="SET",
                values=[BMAssignment(variable=var, numvalue=value)],
            )
        )
    return var


def limit(condition: BMLimitCondition, action: BMAction):
    return BMLimit(condition=condition, action=action)
