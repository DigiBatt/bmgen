from dataclasses import dataclass, field
from bmgen.targets.neware.constants import (
    StepType,
    Factor,
    LimitType,
    StepColors,
    RecordType,
    NewareAction,
)
import xml.etree.ElementTree as ee
from typing import List, Dict
from datetime import datetime
import bmgen


@dataclass
class NewareLimit:
    type: LimitType
    value: float
    action: NewareAction = NewareAction.NextStep


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

    def _timestring(self):
        t = self.steptime
        if t == None:
            return ""
        hours = int(t / 3600)
        t -= hours * 3600
        minutes = int(t / 60)
        t -= minutes * 60
        return f"{hours}:{minutes:02d}:{t:06.3f}"

    def _str(self, value):
        if value == None:
            return ""
        return str(value)

    def toTable(self, linenumber):
        if self.operator in StepColors:
            color = StepColors[self.operator]
        else:
            color = "#000000"
        stepname = str(self.operator).split(".")[1].replace("_", " ")
        steptime = self._timestring()
        voltage = self._str(self.voltage)
        current = self._str(self.current)
        cutoffVoltage = self._str(self.cutoffVoltage)
        cutoffCurrent = self._str(self.cutoffCurrent)
        capacity = self._str(self.capacity)
        return f'<tr style="color: {color}"><td>{linenumber}</td><td>{stepname}</td><td>{steptime}</td><td>{voltage}</td><td>{current}</td><td>{cutoffVoltage}</td><td>{cutoffCurrent}</td><td>{capacity}</td><td></td></tr>\n'


@dataclass
class NewareProgram:
    lines: List[NewareStatement] = field(default_factory=list)
    protections: Dict[LimitType, float] = field(default_factory=dict)
    record: Dict[RecordType, float] = field(default_factory=dict)

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

        # record settings
        if not self.record:
            self.record[RecordType.Time] = 1

        record = ee.SubElement(whole, "Record")
        mainr = ee.SubElement(record, "Main")
        if RecordType.Time in self.record:
            _addLimit(mainr, "Time", self.record[RecordType.Time], Factor.Time)
        if RecordType.Voltage in self.record:
            _addLimit(mainr, "Volt", self.record[RecordType.Voltage], Factor.Voltage)
        if RecordType.Current in self.record:
            _addLimit(mainr, "Curr", self.record[RecordType.Current], Factor.Current)

        return whole

    def toXML(self):
        header = self._header()
        preface = self._preface()
        root = ee.Element("root")
        if bmgen.options["no-timestamps"]:
            timestamp = "0"
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        conf = ee.SubElement(
            root,
            "config",
            {
                "version": "16",
                "type": "Step File",
                "client_version": "BTS Client 8.0.0.484(2021.08.25)(R3)",
                "date": timestamp,
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

    # def mainChannelTable(self):
    #     table = "<table>\n<tr><th>Step Index</th><th>Step Name</th><th>Step Time (hh:mm:ss.ms)</th><th>Voltage (V)</th><th>Current (A)</th><th>Cutoff voltage (V)</th><th>Cutoff current (A)</th><th>Capacity (Ah)</th><th>Others</th></tr>\n"

    def toTable(self):
        table = '<html><head><style type="text/css">table, th, td { border: 1px solid black; border-collapse: collapse; vertical-align: top; text-align: center; } table {float: left}</style></head><body>'
        table += "<table>\n<tr><th>Step Index</th><th>Step Name</th><th>Step Time (hh:mm:ss.ms)</th><th>Voltage (V)</th><th>Current (A)</th><th>Cutoff voltage (V)</th><th>Cutoff current (A)</th><th>Capacity (Ah)</th><th>Others</th></tr>\n"
        for i, line in enumerate(self.lines, 1):
            table += line.toTable(i)
        table += "</table>"
        # table += self.mainChannelTable()
        table += "</body></html>"
        return table


def _addLimit(limitMain, name, value, factor):
    return ee.SubElement(
        limitMain, name, {"Is_Select": "1", "Value": str(int(value * factor))}
    )
