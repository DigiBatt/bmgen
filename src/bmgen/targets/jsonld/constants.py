import bmgen.targets.jsonld.ontology as ontology

LOWER_LIMITS = {
    ontology.CellCurrent: ontology.TerminationQuantity,
    ontology.CellVoltage: ontology.LowerVoltageLimit,
}

UPPER_LIMITS = {
    ontology.CellCurrent: ontology.TerminationQuantity,
    ontology.CellVoltage: ontology.UpperVoltageLimit,
}

TERMINATION_UNITS = {
    "ElectricCurrent": "Ampere",
    "Voltage": "Volt",
    "time": "Second",
    "charge": "AmpereHour",
}
