from bmgen.targets.bm.ast import BMVariable
from bmgen.battery import CyclerBattery

battery = CyclerBattery(
    nominalCapacity=BMVariable("CNom"),
    maxVoltage=BMVariable("UMax"),
    minVoltage=BMVariable("UNom"),
    eocVoltage=BMVariable("UGas"),
    eodVoltage=BMVariable("CutOff"),
    contChargeCurrent=BMVariable("ChargeF"),
    contDischargeCurrent=BMVariable("ICrank"),
    nominalCurrent=BMVariable("INom"),
    internalResistance=BMVariable("Rin"),
    energyDensity=BMVariable("EDensity"),
    oneC=BMVariable("ACn1"),
)
