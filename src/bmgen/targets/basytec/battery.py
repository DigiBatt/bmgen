from bmgen.targets.basytec.ast import BasytecValueLiteral, BasytecUnit
from bmgen.battery import CyclerBattery

battery = CyclerBattery(
    nominalCapacity=BasytecValueLiteral(1, BasytecUnit("CN")),
    minVoltage=BasytecValueLiteral(1, BasytecUnit("UBatMin")),
    maxVoltage=BasytecValueLiteral(1, BasytecUnit("UBatMax")),
    nominalVoltage=BasytecValueLiteral(1, BasytecUnit("UN")),
    eodVoltage=BasytecValueLiteral(1, BasytecUnit("UBatDch")),
    eocVoltage=BasytecValueLiteral(1, BasytecUnit("UBatCh")),
    contChargeCurrent=BasytecValueLiteral(1, BasytecUnit("IBatCh")),
    peakChargeCurrent=BasytecValueLiteral(1, BasytecUnit("IBatMax")),
    contDischargeCurrent=BasytecValueLiteral(1, BasytecUnit("IBatDch")),
    peakDischargeCurrent=BasytecValueLiteral(1, BasytecUnit("IBatMin")),
    oneC=BasytecValueLiteral(1, BasytecUnit("CA")),
)
