from enum import Enum


class StepType(Enum):
    CC_Chg = 1
    CC_DChg = 2
    CV_Chg = 3
    Rest = 4
    Cycle = 5
    End = 6
    CCCV_Chg = 7
    CP_DChg = 8
    CP_Chg = 9
    CR_DChg = 10
    TBD6 = 11
    TBD7 = 12
    TBD8 = 13
    TBD9 = 14
    TBD10 = 15
    Pulse = 16
    SIM = 17
    PCCCV_Chg = 18
    CV_DChg = 19
    CCCV_DChg = 20


class Factor:
    Time = 1000
    Voltage = 10000
    Current = 100000
    Capacity = 60 * 60 * 100000


class LimitType(Enum):
    VoltageLower = 1
    VoltageUpper = 2
    CurrentLower = 3
    CurrentUpper = 4
    CapacityUpper = 5
    Time = 6


class Colors(str, Enum):
    Green = "#81bc06"
    Yellow = "#eec908"
    Red = "#f35325"


StepColors = {
    StepType.CC_Chg: Colors.Green,
    StepType.CC_DChg: Colors.Red,
    StepType.CV_Chg: Colors.Green,
    StepType.Rest: Colors.Yellow,
    StepType.CCCV_Chg: Colors.Green,
    StepType.CP_DChg: Colors.Red,
    StepType.CP_Chg: Colors.Green,
    StepType.CR_DChg: Colors.Red,
    StepType.PCCCV_Chg: Colors.Green,
    StepType.CV_DChg: Colors.Red,
    StepType.CCCV_DChg: Colors.Red,
}


class RecordType(Enum):
    Time = 1
    Voltage = 2
    Current = 3


class NewareAction(Enum):
    Finished = 1
    Protected = 2
    Stop = 3
    NextStep = 4


class NewareOtherType(Enum):
    Expression = 22
    Set = 23


class NewareComparator(Enum):
    Greater = 3
    Nothing = 4
    Less = 5


class NewareGlobalVariable(Enum):
    Voltage = 1
    VolMax = 2
    VolMin = 3
    Current = 4
    CurrMax = 5
    CurrMin = 6
    StepTime = 7
    TestTime = 8
    Ah = 9
    ChargeAh = 10
    DischargeAh = 11
    Wh = 12
    ChargeWh = 13
    DischargeWh = 14


class NewareGotoTarget(Enum):
    Nothing = 0
    Next = 65526


NewareComparatorNames = {
    NewareComparator.Greater: ">",
    NewareComparator.Nothing: "",
    NewareComparator.Less: "<",
}

NewareGotoNames = {
    NewareGotoTarget.Nothing: "",
    NewareGotoTarget.Next: "next line",
}

FirstUserVariableId = 71
ExpressionVariableId = 2147483647
