from bmgen.battery import CyclerBattery
from bmgen.targets.bcl.ast import BCLUnit

battery = CyclerBattery(
    oneC=BCLUnit("CRate"),
)
