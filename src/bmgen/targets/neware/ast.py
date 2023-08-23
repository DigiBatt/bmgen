from dataclasses import dataclass, field
from bmgen.targets.neware.constants import StepType, Factor, LimitType
import xml.etree.ElementTree as ee
from typing import List, Dict
from datetime import datetime


@dataclass
class NewareLimit:
    type: LimitType
    value: float
    protection: bool


@dataclass
class NewareStatement:
    operator: StepType
    steptime: float | None = None
    voltage: float | None = None
    current: float | None = None
    cutoffVoltage: float | None = None
    cutoffCurrent: float | None = None
    capacity: float | None = None
    others: str | None = None

    def toXML(self, linenumber: int):
        step = ee.Element(
            f"Step{linenumber}",
            {"Step_ID": str(linenumber), "Step_Type": str(self.operator.value)},
        )
        limit = ee.SubElement(step, "Limit")
        limitMain = ee.SubElement(limit, "Main")
        if self.steptime != None:
            _addLimit(limitMain, "Time", self.steptime, Factor.Time)
        if self.voltage != None:
            _addLimit(limitMain, "Volt", self.voltage, Factor.Voltage)
        if self.current != None:
            _addLimit(limitMain, "Curr", self.current, Factor.Current)
        if self.capacity != None:
            _addLimit(limitMain, "Cap", self.capacity, Factor.Capacity)
        if self.cutoffVoltage != None:
            _addLimit(limitMain, "Stop_Volt", self.cutoffVoltage, Factor.Voltage)
        if self.cutoffCurrent != None:
            _addLimit(limitMain, "Stop_Curr", self.cutoffCurrent, Factor.Current)

        if self.others:
            raise NotImplementedError("Other Neware limits not yet implemented")

        advamced = ee.SubElement(step, "AdvancedPrt")
        advancedCV = ee.SubElement(advamced, "CV_Chg")
        ee.SubElement(advancedCV, "CurrRise", {"Count": "0"})
        ee.SubElement(advamced, "Safe", {"N2GroupCount": "0"})

        return step


@dataclass
class NewareProgram:
    lines: List[NewareStatement] = field(default_factory=list)
    protections: Dict[LimitType, float] = field(default_factory=dict)

    def _header(self):
        header = ee.Element("Head_Info")
        ee.SubElement(header, "Operate", {"Value": "66"})
        ee.SubElement(header, "Scale", {"Value": "100"})
        ee.SubElement(header, "Start_Step", {"Value": "1", "Hide_Ctrl_Step": "0"})
        ee.SubElement(header, "Creator", {"Value": ""})
        ee.SubElement(header, "PN", {"Value": ""})
        ee.SubElement(header, "Remark", {"Value": ""})
        ee.SubElement(header, "RateType", {"Value": "103"})

        return header

    def _preface(self):
        whole = ee.Element("Whole_Prt")

        # protection settings
        protect = ee.SubElement(whole, "Protect")
        main = ee.SubElement(protect, "Main")

        # voltage
        if (
            LimitType.VoltageLower in self.protections
            or LimitType.VoltageUpper in self.protections
        ):
            volt = ee.SubElement(main, "Volt")
            if LimitType.VoltageLower in self.protections:
                value = self.protections[LimitType.VoltageLower]
                _addLimit(volt, "Lower", value, Factor.Voltage)
            if LimitType.VoltageUpper in self.protections:
                value = self.protections[LimitType.VoltageUpper]
                _addLimit(volt, "Upper", value, Factor.Voltage)

        # current
        if (
            LimitType.CurrentLower in self.protections
            or LimitType.CurrentUpper in self.protections
        ):
            curr = ee.SubElement(main, "Curr")
            if LimitType.CurrentLower in self.protections:
                value = self.protections[LimitType.CurrentLower]
                _addLimit(curr, "Lower", value, Factor.Current)
            if LimitType.CurrentUpper in self.protections:
                value = self.protections[LimitType.CurrentUpper]
                _addLimit(curr, "Upper", value, Factor.Current)

        # capacity
        if LimitType.CapacityUpper in self.protections:
            cap = ee.SubElement(main, "Cap")
            value = self.protections[LimitType.CapacityUpper]
            _addLimit(cap, "Upper", value, Factor.Capacity)

        # delay
        if LimitType.Time in self.protections:
            value = self.protections[LimitType.Time]
            _addLimit(main, "Delay", value, Factor.Time)

        return whole

    def toXML(self):
        header = self._header()
        preface = self._preface()
        root = ee.Element("root")
        conf = ee.SubElement(
            root,
            "config",
            {
                "version": "16",
                "type": "Step File",
                "client_version": "BTS Client 8.0.0.484(2021.08.25)(R3)",
                "date": datetime.now().strftime("%Y%m%d%H%M%S"),
                "Guid": "0045b3d2-59aa-4cb0-9cb8-6a7d7895c0a3",
            },
        )
        conf.append(header)
        conf.append(preface)
        stepinfo = ee.Element("Step_Info", {"Num": str(len(self.lines))})
        for i, line in enumerate(self.lines, 1):
            stepinfo.append(line.toXML(i))
        conf.append(stepinfo)

        smbus = ee.SubElement(conf, "SMBUS")
        ee.SubElement(smbus, "SMBUS_Path", {"Values": ""})
        ee.SubElement(smbus, "SMBUS_Info", {"Num": "0", "AdjacentInterval": "0"})

        return ee.tostring(root, "unicode")


def _addLimit(limitMain, name, value, factor):
    return ee.SubElement(
        limitMain, name, {"Is_Select": "1", "Value": str(int(value * factor))}
    )
