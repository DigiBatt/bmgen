# from bmgen import battery
from bmgen.function import charge, discharge, pause, time
from bmgen import battery
from bmgen.channel import I, V

CRate = 0.5
EOCCurrent = 0.05
PauseLen = [1, 1.5, 2]

PauseLen[1] = 5

for i in range(3):
    charge(
        CRate * battery.nominalCapacity,
        voltage=4.2,
        limits=[I < EOCCurrent],
    )
    pause(limits=[time(hours=PauseLen[i])])
    if i < 2:
        discharge(CRate * battery.nominalCapacity, limits=[V <= 2.5])
    CRate += 0.2
