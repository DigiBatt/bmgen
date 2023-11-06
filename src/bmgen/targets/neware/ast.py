from dataclasses import dataclass, field
import bmgen.targets.neware.constants as constants
import xml.etree.ElementTree as ee
from typing import List, Dict
from datetime import datetime
import bmgen


@dataclass
class NewareLimit:
    type: constants.LimitType
    value: float
    action: constants.NewareAction = constants.NewareAction.NextStep


@dataclass
class NewareExpressionString:
    expression: str


@dataclass
class NewareOther:
    type: constants.NewareOtherType
    userVariableId: int
    globalVariable: constants.NewareGlobalVariable | int
    comparator: constants.NewareComparator = constants.NewareComparator.Nothing
    goto: constants.NewareGotoTarget = constants.NewareGotoTarget.Nothing
    expressionName: str | None = None
    expression: NewareExpressionString | None = None

    def toXML(self, parent, number):
        attr = {
            "type": str(self.type.value),
            "Function": "0",
            "CmpType": str(self.comparator.value),
            "Jump_Line": str(self.goto.value),
            "Value": "0",
            "TimeGoto": "0",
            "GlobleUserID": str(self.userVariableId),
            "GLobleType": "1",
            "Aux": "0",
        }
        if isinstance(self.globalVariable, constants.NewareGlobalVariable):
            attr["GlobalVar"] = str(self.globalVariable.value)
        else:
            attr["GlobalVar"] = str(self.globalVariable)
        if self.expressionName:
            attr["ExpressionName"] = self.expressionName
        if self.expression:
            attr["Expression"] = self.expression.expression
        return ee.SubElement(parent, f"Cnd{number}", attr)

    def toText(self):
        raise NotImplementedError()


@dataclass
class NewareSet(NewareOther):
    def __init__(
        self, userVariableId: int, globalVariable: constants.NewareGlobalVariable
    ):
        super().__init__(constants.NewareOtherType.Set, userVariableId, globalVariable)

    def toText(self):
        return f"SET User{self.userVariableId - constants.FirstUserVariableId + 1} = {self.globalVariable.name}"


@dataclass
class NewareExpression(NewareOther):
    def __init__(
        self,
        userVariableId: int,
        globalVariable: int,
        expressionName: str,
        expression: NewareExpressionString,
        comparator: constants.NewareComparator,
        goto: constants.NewareGotoTarget,
    ):
        super().__init__(
            constants.NewareOtherType.Expression,
            userVariableId,
            globalVariable,
            expressionName=expressionName,
            expression=expression,
            comparator=comparator,
            goto=goto,
        )

    def toText(self):
        return f"IF {self.expression.expression} {constants.NewareComparatorNames[self.comparator]} 0 GOTO {constants.NewareGotoNames[self.goto]}"


@dataclass
class NewareStatement:
    operator: constants.StepType
    steptime: float | None = None
    voltage: float | None = None
    current: float | None = None
    cutoffVoltage: float | None = None
    cutoffCurrent: float | None = None
    capacity: float | None = None
    others: List[NewareOther] = field(default_factory=list)
    record: Dict[constants.RecordType, float] = field(default_factory=dict)

    def toXML(self, linenumber: int):
        step = ee.Element(
            f"Step{linenumber}",
            {"Step_ID": str(linenumber), "Step_Type": str(self.operator.value)},
        )
        limit = ee.SubElement(step, "Limit")
        limitMain = ee.SubElement(limit, "Main")
        if self.steptime != None:
            _addLimit(limitMain, "Time", self.steptime, constants.Factor.Time)
        if self.voltage != None:
            _addLimit(limitMain, "Volt", self.voltage, constants.Factor.Voltage)
        if self.current != None:
            _addLimit(limitMain, "Curr", self.current, constants.Factor.Current)
        if self.capacity != None:
            _addLimit(limitMain, "Cap", self.capacity, constants.Factor.Capacity)
        if self.cutoffVoltage != None:
            _addLimit(
                limitMain, "Stop_Volt", self.cutoffVoltage, constants.Factor.Voltage
            )
        if self.cutoffCurrent != None:
            _addLimit(
                limitMain, "Stop_Curr", self.cutoffCurrent, constants.Factor.Current
            )

        if self.others:
            limitOther = ee.SubElement(
                limit, "Other", {"CndCount": str(len(self.others))}
            )
            for n, o in enumerate(self.others, 1):
                o.toXML(limitOther, n)

        advamced = ee.SubElement(step, "AdvancedPrt")
        advancedCV = ee.SubElement(advamced, "CV_Chg")
        ee.SubElement(advancedCV, "CurrRise", {"Count": "0"})
        ee.SubElement(advamced, "Safe", {"N2GroupCount": "0"})

        if self.record:
            record = ee.SubElement(step, "Record")
            mainr = ee.SubElement(record, "Main")
            if constants.RecordType.Time in self.record:
                _addLimit(
                    mainr,
                    "Time",
                    self.record[constants.RecordType.Time],
                    constants.Factor.Time,
                )
            if constants.RecordType.Voltage in self.record:
                _addLimit(
                    mainr,
                    "Volt",
                    self.record[constants.RecordType.Voltage],
                    constants.Factor.Voltage,
                )
            if constants.RecordType.Current in self.record:
                _addLimit(
                    mainr,
                    "Curr",
                    self.record[constants.RecordType.Current],
                    constants.Factor.Current,
                )

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
        if self.operator in constants.StepColors:
            color = constants.StepColors[self.operator]
        else:
            color = "#000000"
        stepname = str(self.operator).split(".")[1].replace("_", " ")
        steptime = self._timestring()
        voltage = self._str(self.voltage)
        current = self._str(self.current)
        cutoffVoltage = self._str(self.cutoffVoltage)
        cutoffCurrent = self._str(self.cutoffCurrent)
        capacity = self._str(self.capacity)
        others = "<br>".join([o.toText() for o in self.others])
        return f'<tr style="color: {color}"><td>{linenumber}</td><td>{stepname}</td><td>{steptime}</td><td>{voltage}</td><td>{current}</td><td>{cutoffVoltage}</td><td>{cutoffCurrent}</td><td>{capacity}</td><td>{others}</td></tr>\n'


@dataclass
class NewareProgram:
    lines: List[NewareStatement] = field(default_factory=list)
    protections: Dict[constants.LimitType, float] = field(default_factory=dict)
    record: Dict[constants.RecordType, float] = field(default_factory=dict)

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
            constants.LimitType.VoltageLower in self.protections
            or constants.LimitType.VoltageUpper in self.protections
        ):
            volt = ee.SubElement(main, "Volt")
            if constants.LimitType.VoltageLower in self.protections:
                value = self.protections[constants.LimitType.VoltageLower]
                _addLimit(volt, "Lower", value, constants.Factor.Voltage)
            if constants.LimitType.VoltageUpper in self.protections:
                value = self.protections[constants.LimitType.VoltageUpper]
                _addLimit(volt, "Upper", value, constants.Factor.Voltage)

        # current
        if (
            constants.LimitType.CurrentLower in self.protections
            or constants.LimitType.CurrentUpper in self.protections
        ):
            curr = ee.SubElement(main, "Curr")
            if constants.LimitType.CurrentLower in self.protections:
                value = self.protections[constants.LimitType.CurrentLower]
                _addLimit(curr, "Lower", value, constants.Factor.Current)
            if constants.LimitType.CurrentUpper in self.protections:
                value = self.protections[constants.LimitType.CurrentUpper]
                _addLimit(curr, "Upper", value, constants.Factor.Current)

        # capacity
        if constants.LimitType.CapacityUpper in self.protections:
            cap = ee.SubElement(main, "Cap")
            value = self.protections[constants.LimitType.CapacityUpper]
            _addLimit(cap, "Upper", value, constants.Factor.Capacity)

        # delay
        if constants.LimitType.Time in self.protections:
            value = self.protections[constants.LimitType.Time]
            _addLimit(main, "Delay", value, constants.Factor.Time)

        # record settings
        if not self.record:
            self.record[constants.RecordType.Time] = 1

        record = ee.SubElement(whole, "Record")
        mainr = ee.SubElement(record, "Main")
        if constants.RecordType.Time in self.record:
            _addLimit(
                mainr,
                "Time",
                self.record[constants.RecordType.Time],
                constants.Factor.Time,
            )
        if constants.RecordType.Voltage in self.record:
            _addLimit(
                mainr,
                "Volt",
                self.record[constants.RecordType.Voltage],
                constants.Factor.Voltage,
            )
        if constants.RecordType.Current in self.record:
            _addLimit(
                mainr,
                "Curr",
                self.record[constants.RecordType.Current],
                constants.Factor.Current,
            )

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
                "version": "17",
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
        table = "<table>\n<tr><th>Step Index</th><th>Step Name</th><th>Step Time (hh:mm:ss.ms)</th><th>Voltage (V)</th><th>Current (A)</th><th>Cutoff voltage (V)</th><th>Cutoff current (A)</th><th>Capacity (Ah)</th><th>Others</th></tr>\n"
        for i, line in enumerate(self.lines, 1):
            table += line.toTable(i)
        table += "</table>"
        # table += self.mainChannelTable()
        return table


def _addLimit(limitMain, name, value, factor):
    return ee.SubElement(
        limitMain, name, {"Is_Select": "1", "Value": str(int(value * factor))}
    )
