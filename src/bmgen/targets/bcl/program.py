from bmgen.targets.bcl.ast import BCLStep
from bmgen.targets.bcl.stepinfo import BCLStepInfo


def variable(name: str, value: float | None = None):
    if isinstance(value, BCLStep):
        return BCLStepInfo(value, name)
    return value
