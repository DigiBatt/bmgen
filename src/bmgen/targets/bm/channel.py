import bmgen
from bmgen.targets.bm.ast import BMChannel, BMChannelDynamic

I = BMChannel("A")
V = BMChannel("V")
StepCharge = BMChannel("AhStep")
T = BMChannelDynamic(
    lambda: __get_with_default(bmgen.options.get("bm", {}), "cell-temperature", "C1")
)
Tenv = BMChannelDynamic(
    lambda: __get_with_default(bmgen.options.get("bm", {}), "env-temperature", "Cenv")
)


def __get_with_default(config, key, default):
    value = config.get(key, None)
    if value is None or not isinstance(value, str) or value.strip() == "":
        return default
    return value


def channel(name: str) -> BMChannel:
    return BMChannel(name)
