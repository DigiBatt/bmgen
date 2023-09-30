from bmgen.targets.basytec.ast import BasytecStatement
from bmgen.targets.basytec.stepinfo import BasytecStepInfo


def variable(name: str, value: float | None = None):
    if isinstance(value, BasytecStatement):
        return BasytecStepInfo(value, name)
    return value
