from bmgen.targets.basytec.ast import BasytecValue, BasytecUnit
from bmgen.battery import CyclerBattery

battery = CyclerBattery(
    nominalCapacity=BasytecValue(1, BasytecUnit("CN")),
    maxVoltage=BasytecValue(1, BasytecUnit("UBatMax")),
    minVoltage=BasytecValue(1, BasytecUnit("UBatMin")),
    eocVoltage=BasytecValue(1, BasytecUnit("UBatCh")),
    eodVoltage=BasytecValue(1, BasytecUnit("UBatDch")),
    oneC=BasytecValue(1, BasytecUnit("CA")),
)
