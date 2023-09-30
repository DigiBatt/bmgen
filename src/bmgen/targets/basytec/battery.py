from bmgen.targets.basytec.ast import BasytecValueLiteral, BasytecUnit
from bmgen.battery import CyclerBattery

battery = CyclerBattery(
    nominalCapacity=BasytecValueLiteral(1, BasytecUnit("CN")),
    maxVoltage=BasytecValueLiteral(1, BasytecUnit("UBatMax")),
    minVoltage=BasytecValueLiteral(1, BasytecUnit("UBatMin")),
    eocVoltage=BasytecValueLiteral(1, BasytecUnit("UBatCh")),
    eodVoltage=BasytecValueLiteral(1, BasytecUnit("UBatDch")),
    oneC=BasytecValueLiteral(1, BasytecUnit("CA")),
)
