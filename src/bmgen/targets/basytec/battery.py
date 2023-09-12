from bmgen.targets.basytec.ast import BasytecValue, BasytecUnit

nominalCapacity = BasytecValue(1, BasytecUnit("CN"))
maxVoltage = BasytecValue(1, BasytecUnit("UBatMax"))
minVoltage = BasytecValue(1, BasytecUnit("UBatMin"))
eocVoltage = BasytecValue(1, BasytecUnit("UBatCh"))
eodVoltage = BasytecValue(1, BasytecUnit("UBatDch"))
