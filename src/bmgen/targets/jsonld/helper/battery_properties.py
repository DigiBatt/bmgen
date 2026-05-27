import bmgen.targets.jsonld.ontology as ontology

BATTERY_PROPERTIES = {
    "nominalCapacity": ontology.NominalCapacity,
    "eocVoltage": ontology.UpperVoltageLimit,
    "eodVoltage": ontology.LowerVoltageLimit,
    "contChargeCurrent": ontology.MaximumContinuousChargingCurrent,
    "contDischargeCurrent": ontology.MaximumContinuousDischargingCurrent,
    "internalResistance": ontology.InternalResistance,
    "energyDensity": ontology.EnergyDensity,
}
