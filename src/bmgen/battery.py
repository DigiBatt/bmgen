from dataclasses import dataclass
from typing import Any


@dataclass
class Battery:
    """This class can be used to reference battery parameters in a cycling program. Parameters can be set to fixed values or translated to variables for the cycler."""

    nominalCapacity: float | None = None  #: Nominal capcity of the battery in Ah.
    minVoltage: float | None = (
        None  #: Lower voltage limit that must not be exceeded in V.
    )
    maxVoltage: float | None = (
        None  #: Upper voltage limit that must not be exceeded in V.
    )
    nominalVoltage: float | None = None  #: Nominal voltage in V
    eodVoltage: float | None = (
        None  #: End-of-discharge voltage for standard discharging in V.
    )
    eocVoltage: float | None = (
        None  #: End-of-charge voltage for standard charging in V.
    )
    contChargeCurrent: float | None = None  #: Maximum constant charge current in A.
    peakChargeCurrent: float | None = None  #: Peak charge current in A.
    contDischargeCurrent: float | None = (
        None  #: Maximum constant discharge current in A.
    )
    peakDischargeCurrent: float | None = None  #: Peak discharge current in A.
    minChargeTemperature: float | None = None  #: Minimum charge temperature in °C.
    maxChargeTemperature: float | None = None  #: Maximum charge temperature in °C.
    minDischargeTemperature: float | None = (
        None  #: Minimum discharge temperature in °C.
    )
    maxDischargeTemperature: float | None = (
        None  #: Maximum discharge temperature in °C.
    )
    weight: float | None = None  #: Weight of the battery in g.
    nominalCurrent: float | None = None  #: Nominal current in A.
    energyDensity: float | None = None  #: Energy density in Wh/l.
    internalResistance: float | None = None  #: Internal resistance in Ohm.
    oneC: float | None = None  #: Current that is equal to 1C in A.


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
