from bmgen.targets.bm.ast import BMVariable
import bmgen

I = BMVariable("A")
V = BMVariable("V")
StepCharge = BMVariable("AhStep")
T = BMVariable(bmgen.options.get("bm", {}).get("cell-temperature", "C1"))
Tenv = BMVariable(bmgen.options.get("bm", {}).get("env-temperature", "Cenv"))


def channel(name: str) -> BMVariable:
    return BMVariable(name)
