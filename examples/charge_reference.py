from bmgen import battery
from bmgen.channel import *
from bmgen.function import *

cutoffCurrent = 0.05
chargeRate = 0.5
nomCapacityRate = 0.2

charge(chargeRate * battery.oneC, battery.eocVoltage, limits=[I < cutoffCurrent])
dchStep = discharge(nomCapacityRate * battery.oneC, limits=[V < battery.eodVoltage])
charge(chargeRate * battery.oneC, battery.eocVoltage, limits=[I < cutoffCurrent])

lastSoc = 100
for thisSoc in [80, 50, 20]:
    socDiff = (lastSoc - thisSoc) / 100
    discharge(
        chargeRate * battery.oneC,
        limits=[V < battery.eodVoltage, StepCharge > dchStep.charge * socDiff],
    )

    pause(minutes=20)
    charge(5, limits=[time(seconds=30), V > battery.maxVoltage])
    pause(minutes=20)
    discharge(5, limits=[time(seconds=30), V < battery.minVoltage])

    lastSoc = thisSoc
