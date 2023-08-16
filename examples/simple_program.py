# from bmgen import battery
from bmgen.function import charge
from bmgen import battery
from bmgen.channel import I

CRate = 0.5
EOCCurrent = 0.05

for i in range(3):
    charge(
        CRate * battery.nominalCapacity,
        voltage=4.2,
        limits=[I < EOCCurrent],
    )
#     if i < 2:
#         discharge(CRate * battery.nominalCapacity, limit(U <= 2.5))
