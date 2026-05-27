from bmgen.battery import CyclerBattery
from bmgen.targets.jsonld.ast import Reference, NumericLiteral

import bmgen.targets.jsonld.ontology as ontology

battery = CyclerBattery(
    nominalCapacity=Reference("battery_nominal_capacity"),
    maxVoltage=Reference("battery_eoc_voltage"),
    minVoltage=Reference("battery_eod_voltage"),
    eocVoltage=Reference("battery_eoc_voltage"),
    eodVoltage=Reference("battery_eod_voltage"),
    contChargeCurrent=Reference("battery_cont_charge_current"),
    contDischargeCurrent=Reference("battery_cont_discharge_current"),
    internalResistance=Reference("battery_internal_resistance"),
    energyDensity=Reference("battery_energy_density"),
    oneC=NumericLiteral(1, ontology.AmperePerAmpereHour),
)
