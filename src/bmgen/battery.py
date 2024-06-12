from dataclasses import dataclass
from typing import Any


@dataclass
class Battery:
    nominalCapacity: float | None = None
    minVoltage: float | None = None
    maxVoltage: float | None = None
    nominalVoltage: float | None = None
    eodVoltage: float | None = None
    eocVoltage: float | None = None
    contChargeCurrent: float | None = None
    peakChargeCurrent: float | None = None
    contDischargeCurrent: float | None = None
    peakDischargeCurrent: float | None = None
    minChargeTemperature: float | None = None
    maxChargeTemperature: float | None = None
    minDischargeTemperature: float | None = None
    maxDischargeTemperature: float | None = None
    weight: float | None = None
    nominalCurrent: float | None = None
    energyDensity: float | None = None
    internalResistance: float | None = None
    oneC: float | None = None


class CyclerBattery(Battery):
    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if value is None:
            raise Exception(
                f"Battery parameter '{name}' not available for the chosen target"
            )
        return value


class PredefindedBattery(Battery):
    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if name == "oneC" and value is None:
            value = super().__getattribute__("nominalCapacity")
        if value is None:
            raise Exception(
                f"Battery parameter '{name}' not specified in the battery definition"
            )
        return value
