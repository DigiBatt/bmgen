from bmgen.targets.bm.ast import (
    BMVariable,
    BMStatement,
    BMAssignment,
    BMLimit,
    BMLimitCondition,
    BMAction,
    BMNumValue,
    BMNumber,
)
from bmgen.targets.bm import generator
from bmgen.targets.bm.helper.cast import autocast
from typing import List


@autocast("value")
def variable(name: str, value: BMNumValue | List[BMNumValue] | None = None):
    var = BMVariable(name)
    if value:
        if isinstance(value, list):
            arraynum = generator.array()
            generator.add(
                BMStatement(
                    operator="SET",
                    values=[
                        BMAssignment(
                            variable=BMVariable(name + "_IV"),
                            numvalue=BMNumber(123454321 + arraynum),
                        ),
                        BMAssignment(
                            variable=BMVariable(name + "_Val"),
                            numvalue=BMNumber(0),
                        ),
                        *[
                            BMAssignment(
                                variable=BMVariable(name + f"_{i}"),
                                numvalue=v,
                            )
                            for i, v in enumerate(value)
                        ],
                    ],
                )
            )
            var.arraynum = arraynum
        else:
            generator.add(
                BMStatement(
                    operator="SET",
                    values=[BMAssignment(variable=var, numvalue=value)],
                )
            )
    return var
