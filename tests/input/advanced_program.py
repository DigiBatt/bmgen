from bmgen import battery
from bmgen.channel import I, V
from bmgen.function import charge, discharge, pause, range, time

CRate = 0.5
EOCCurrent = 0.05
PauseLen = [1, 1.5, 2]

PauseLen[1] = 5

for i in range(3):
    charge(
        current=CRate * battery.oneC,
        voltage=4.2,
        limits=[I < EOCCurrent, time(hours=5)],
    )
    pause(hours=PauseLen[i])
    if i < 2:
        discharge(
            CRate * battery.oneC,
            limits=[V <= 2.5],
        )
    else:
        discharge(
            CRate * battery.oneC,
            limits=[V <= 2.0],
        )
    CRate += 0.2
