from bmgen.targets.basytec.ast import BasytecChannel, BasytecUnit

I = BasytecChannel("I", BasytecUnit("A"))
V = BasytecChannel("U", BasytecUnit("V"))
t = BasytecChannel("t", BasytecUnit("s"))
StepCharge = BasytecChannel("Ah", BasytecUnit("Ah"))


def channel(name: str) -> BasytecChannel:
    return BasytecChannel(name, BasytecUnit(""))
