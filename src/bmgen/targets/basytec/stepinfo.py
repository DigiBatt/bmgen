from dataclasses import dataclass
from bmgen.targets.basytec.ast import (
    BasytecStatement,
    BasytecCalculation,
    BasytecVariable,
)
import bmgen.targets.basytec as target
from bmgen.targets.basytec.constants import StepType


@dataclass
class BasytecStepInfo:
    step: BasytecStatement
    varname: str
    chargeVar: BasytecVariable | None = None

    @property
    def charge(self):
        if not self.chargeVar:
            self.step.label = self.varname.upper()
            self.chargeVar = BasytecVariable(self.varname + "_chg")
            chargeSaveStep = BasytecStatement(
                StepType.CalcOnce,
                parameters=[
                    BasytecCalculation(
                        variable=self.chargeVar,
                        calculation=f"As_C[{self.varname.upper()}]+As_D[{self.varname.upper()}]",
                    )
                ],
            )
            lines = target.generator.program.lines
            stepIdx = lines.index(self.step)
            lines.insert(stepIdx + 1, chargeSaveStep)
        return self.chargeVar
