from bmgen import battery
from bmgen.channel import *
from bmgen.function import *

for iCycle in range(50):
    charge(2, limits=[V > battery.eocVoltage])
    discharge(2, limits=[V < battery.eodVoltage])

for current in [1, 2, 5]:
    charge(current, limits=[V > battery.eocVoltage])
    discharge(current, limits=[V < battery.eodVoltage])



