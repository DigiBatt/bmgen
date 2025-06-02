from dataclasses import dataclass

import bmgen.targets.bcl.ast as ast


@dataclass
class BCLStepInfo:
    step: ast.BCLStep
    varname: str

    @property
    def charge(self):
        return ast.BCLUnit("stepReferenceTest")
