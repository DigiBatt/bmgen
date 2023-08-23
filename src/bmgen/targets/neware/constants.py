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


LimitArgs = {
    LimitType.VoltageLower: "voltage",
    LimitType.VoltageUpper: "voltage",
    LimitType.CurrentLower: "cutoffCurrent",
    LimitType.CurrentUpper: "current",
    LimitType.CapacityUpper: "capacity",
    LimitType.Time: "steptime",
}
