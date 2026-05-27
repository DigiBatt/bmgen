from bmgen.battery import BatteryParametersNotSupported
from bmgen.targets.bcl.ast import BCLUnit

battery = BatteryParametersNotSupported(
    oneC=BCLUnit("CRate"),
)
