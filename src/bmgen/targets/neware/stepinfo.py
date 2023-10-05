from dataclasses import dataclass
from bmgen.targets.neware.ast import NewareStatement, NewareSet, NewareExpressionString
import bmgen.targets.bm as target
import bmgen.targets.neware.constants as constants


@dataclass
class NewareStepInfo:
    step: NewareStatement

    @property
    def charge(self):
        varId = constants.FirstUserVariableId
        self.step.others.append(NewareSet(varId, constants.NewareGlobalVariable.Ah))
        return NewareExpressionString(
            f"User{varId - constants.FirstUserVariableId + 1}"
        )
