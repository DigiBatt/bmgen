from typing import List

import bmgen
import bmgen.targets.bm as target
from bmgen.targets.bm.ast import (
    BMArray,
    BMAssignment,
    BMLimit,
    BMNumber,
    BMNumValue,
    BMStatement,
    BMTwoValues,
    BMVariable,
)
from bmgen.targets.bm.helper.cast import autocast
from bmgen.targets.bm.stepinfo import BMStepInfo


@autocast("value")
def variable(name: str, value: BMNumValue | List[BMNumValue] | None = None):
    var = BMVariable(name)
    if value:
        if isinstance(value, BMStatement):
            return BMStepInfo(value, name)
        if isinstance(value, BMLimit):
            return value
        elif bmgen.options.get("bm", {}).get("pythonEval", False):
            return value
        elif isinstance(value, list):
            arraynum = target.generator.array()
            if bmgen.options.get("bm", {}).get("pythonArrays", False):
                return value
            elif bmgen.options.get("bm", {}).get("oldArrays", False):
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
            else:
                target.generator.add(
                    BMStatement(
                        operator="ARRINIT",
                        values=[BMVariable(name), *value],
                    )
                )
            return BMArray(name, arraynum, len(value))
        elif not (isinstance(value, BMVariable) and value.name == name):
            target.generator.add(
                BMStatement(
                    operator="SET",
                    values=[BMAssignment(variable=var, numvalue=value)],
                )
            )
    return var
