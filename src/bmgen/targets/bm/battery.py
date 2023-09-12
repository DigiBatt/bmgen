from bmgen.targets.bm.ast import BMVariable

nominalCapacity = BMVariable("ACn1")
maxVoltage = BMVariable("UMax")
minVoltage = BMVariable("UNom")
eocVoltage = BMVariable("UGas")
eodVoltage = BMVariable("CutOff")
contChargeCurrent = BMVariable("ChargeF")
contDischargeCurrent = BMVariable("ICrank")
nominalCurrent = BMVariable("INom")
internalResistance = BMVariable("Rin")
energyDensity = BMVariable("EDensity")
