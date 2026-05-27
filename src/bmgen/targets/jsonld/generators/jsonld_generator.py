from typing import List

from bmgen.base_generator import BaseGenerator
from bmgen.targets.jsonld.ast import Program, Step, create_property, Reference
from bmgen.targets.jsonld import battery
import bmgen.targets.jsonld.ontology as ontology


class JSONLDGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = Program([])

    def finish(self):
        pass

    def add(self, step):
        self.program.steps.append(step)
        return step

    def ast(self):
        self.finish()
        return str(self.program)

    def generate_battery(self):
        return ontology.Battery(
            hasProperty=[
                create_property(
                    ontology.NominalCapacity, Reference("battery_nominal_capacity")
                ),
                create_property(
                    ontology.UpperVoltageLimit, Reference("battery_eoc_voltage")
                ),
                create_property(
                    ontology.LowerVoltageLimit, Reference("battery_eod_voltage")
                ),
                create_property(
                    ontology.MaximumContinuousChargingCurrent,
                    Reference("battery_cont_charge_current"),
                ),
                create_property(
                    ontology.MaximumContinuousDischargingCurrent,
                    Reference("battery_cont_discharge_current"),
                ),
                create_property(
                    ontology.InternalResistance,
                    Reference("battery_internal_resistance"),
                ),
                create_property(
                    ontology.EnergyDensity, Reference("battery_energy_density")
                ),
            ]
        )

    def generate(self):
        self.finish()
        program = self.program.toOntology()
        program.hasParticipant = self.generate_battery()
        return program
