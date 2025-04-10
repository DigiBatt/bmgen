from bmgen import battery
from bmgen.channel import *
from bmgen.function import *

cutoffCurrent = 0.05
chargeRate = 0.5

charge(
    chargeRate * battery.oneC,
    battery.eocVoltage,
    limits=[I < cutoffCurrent],
)
