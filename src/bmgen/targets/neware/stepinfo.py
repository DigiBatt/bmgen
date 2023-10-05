from dataclasses import dataclass
from bmgen.targets.neware.ast import NewareStatement, NewareSet, NewareExpressionString
import bmgen.targets.neware as target
import bmgen.targets.neware.constants as constants


@dataclass
class NewareStepInfo:
    step: NewareStatement

    @property
    def charge(self):
        varId = None
        for o in self.step.others:
            if (
                isinstance(o, NewareSet)
                and o.globalVariable == constants.NewareGlobalVariable.Ah
            ):
                varId = o.userVariableId
        if varId == None:
            varId = target.generator.userVar()
            self.step.others.append(NewareSet(varId, constants.NewareGlobalVariable.Ah))
        return NewareExpressionString(
            f"User{varId - constants.FirstUserVariableId + 1}"
        )
