from bmgen.targets.neware.stepinfo import NewareStepInfo
from bmgen.targets.neware.ast import NewareStatement


def variable(name: str, value: float | NewareStatement | None = None):
    if isinstance(value, NewareStatement):
        return NewareStepInfo(value)
    else:
        return value
