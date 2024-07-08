import bmgen
from bmgen.targets.bm.ast import BMChannel

I = BMChannel("A")
V = BMChannel("V")
StepCharge = BMChannel("AhStep")
T = BMChannel(bmgen.options.get("bm", {}).get("cell-temperature", "C1"))
Tenv = BMChannel(bmgen.options.get("bm", {}).get("env-temperature", "Cenv"))


def channel(name: str) -> BMChannel:
    return BMChannel(name)
