from dataclasses import dataclass

import bmgen.targets.bm as target
from bmgen.targets.bm.ast import BMAssignment, BMStatement, BMVariable


@dataclass
class BMStepInfo:
    step: BMStatement
    varname: str
    chargeVar: BMVariable | None = None

    @property
    def charge(self):
        if not self.chargeVar:
            self.chargeVar = BMVariable(self.varname + "_chg")
            chargeSaveStep = BMStatement(
                "SET",
                values=[
                    BMAssignment(variable=self.chargeVar, numvalue=BMVariable("AhStep"))
                ],
            )
            lines = target.generator.program.lines
            stepIdx = lines.index(self.step)
            lines.insert(stepIdx + 1, chargeSaveStep)
        return self.chargeVar
