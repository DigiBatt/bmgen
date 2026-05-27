import bmgen.targets.jsonld.ast as ast

import bmgen.targets.jsonld.ontology as ontology

I = ast.Channel(ontology.CellCurrent, ontology.Ampere)
V = ast.Channel(ontology.CellVoltage, ontology.Volt)
t = ast.Channel(ontology.StepTime, ontology.Second)
# StepCharge = ast.BCLTerminationType("charge")
