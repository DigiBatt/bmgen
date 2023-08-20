# from bmgen import battery
from bmgen.function import charge, discharge
from bmgen import battery
from bmgen.channel import I, V

CRate = 0.5
EOCCurrent = 0.05

for i in range(3):
    charge(
        CRate * battery.nominalCapacity,
        voltage=4.2,
        limits=[I < EOCCurrent],
    )
    if i < 2:
        discharge(CRate * battery.nominalCapacity, limits=[V <= 2.5])
