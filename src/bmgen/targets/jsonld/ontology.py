class OntologyClass:

    attributes: dict

    def __setattr__(self, name, value):
        if not hasattr(self, "attributes"):
            super().__setattr__("attributes", dict())
        self.attributes[name] = value

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def to_jsonld(self):
        jsonld = {"@type": self.__class__.__name__}
        for attr, value in self.attributes.items():
            if isinstance(value, OntologyClass):
                jsonld[attr] = value.to_jsonld()
            elif isinstance(value, list):
                jsonld[attr] = [v.to_jsonld() for v in value]
            else:
                jsonld[attr] = value
        return jsonld


class ElectrochemicalQuantity(OntologyClass):

    def __init__(self, value, unit):
        if value is not None:
            self.hasNumericalPart = {"@type": "RealData", "hasNumberValue": value}
        if unit is not None:
            self.hasMeasurementUnit = {"@type": unit}


class MeasurementUnit(OntologyClass):
    pass


class Procedure(OntologyClass):
    pass


class BatteryTest(OntologyClass):
    pass


class IterativeWorkflow(OntologyClass):
    pass


class Voltage(ElectrochemicalQuantity):
    pass


class ElectricCurrent(ElectrochemicalQuantity):
    pass


class ElectricCharge(ElectrochemicalQuantity):
    pass


class ElectricResistance(ElectrochemicalQuantity):
    pass


class EnergyDensity(ElectrochemicalQuantity):
    pass


class ChargingCurrent(ElectrochemicalQuantity):
    pass


class ChargingVoltage(ElectrochemicalQuantity):
    pass


class ChargingCRate(ElectrochemicalQuantity):
    pass


class DischargingCurrent(ElectrochemicalQuantity):
    pass


class DischargingCRate(ElectrochemicalQuantity):
    pass


class CRateUnit(OntologyClass):
    pass


class NominalCapacity(ElectrochemicalQuantity):
    pass


class UpperVoltageLimit(ElectrochemicalQuantity):
    pass


class LowerVoltageLimit(ElectrochemicalQuantity):
    pass


class MaximumContinuousChargingCurrent(ElectrochemicalQuantity):
    pass


class MaximumContinuousDischargingCurrent(ElectrochemicalQuantity):
    pass


class InternalResistance(ElectrochemicalQuantity):
    pass


class ConstantCurrentConstantVoltageCharging(OntologyClass):
    pass


class ConstantCurrentCharging(OntologyClass):
    pass


class ConstantCurrentDischarging(OntologyClass):
    pass


class ConstantCurrentConstantVoltageDischarging(OntologyClass):
    pass


class DischargingVoltage(OntologyClass):
    pass


class Ampere:
    pass


class Volt:
    pass


class Second:
    pass


class StepDuration(ElectrochemicalQuantity):
    pass


class StepTime(ElectrochemicalQuantity):
    pass


class CellCurrent(ElectrochemicalQuantity):
    pass


class CellVoltage(ElectrochemicalQuantity):
    pass


class AmperePerAmpereHour:
    pass


class Battery(OntologyClass):
    pass


class TerminationQuantity(ElectrochemicalQuantity):
    pass
