from bmgen.targets.bm.ast import (
    BMVariable,
    BMStatement,
    BMAssignment,
    BMNumValue,
    BMNumber,
    BMArray,
)
import bmgen.targets.bm as target
from bmgen.targets.bm.helper.cast import autocast
from typing import List
from bmgen.targets.bm.stepinfo import BMStepInfo


@autocast("value")
def variable(name: str, value: BMNumValue | List[BMNumValue] | None = None):
    var = BMVariable(name)
    if value:
        if isinstance(value, list):
            arraynum = target.generator.array()
            target.generator.add(
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
            return BMArray(name, arraynum, len(value))
        elif isinstance(value, BMStatement):
            return BMStepInfo(value, name)
        else:
            target.generator.add(
                BMStatement(
                    operator="SET",
                    values=[BMAssignment(variable=var, numvalue=value)],
                )
            )
    return var
