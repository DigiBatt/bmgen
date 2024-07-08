import bmgen.targets.bm.ast as ast
from bmgen.battery import CyclerBattery

battery = CyclerBattery(
    nominalCapacity=ast.BMVariable("CNom"),
    maxVoltage=ast.BMVariable("UMax"),
    minVoltage=ast.BMVariable("UNom"),
    eocVoltage=ast.BMVariable("UGas"),
    eodVoltage=ast.BMVariable("CutOff"),
    contChargeCurrent=ast.BMVariable("ChargeF"),
    contDischargeCurrent=ast.BMVariable("ICrank"),
    nominalCurrent=ast.BMVariable("INom"),
    internalResistance=ast.BMVariable("Rin"),
    energyDensity=ast.BMVariable("EDensity"),
    oneC=ast.BMChannel("ACn1"),
)
