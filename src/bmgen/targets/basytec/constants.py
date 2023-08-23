from enum import Enum


class StepType(Enum):
    Charge = 1
    Discharge = 2
    Pause = 3
    Ramp_I = 4
    Ramp_U = 5
    Set = 6
    Set_Temp = 7
    Cycle_start = 8
    Cycle_end = 9
    Table = 10
    Calculate = 11
    CalcOnce = 12
    Const = 13
    EIS = 14
    Result = 15
    Start = 16
    Stop = 17
    Extern = 18
    Define = 19
    Message = 20


Newline = "\xfe\xfd"
