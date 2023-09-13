# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *
from bmgen import battery

# set safety limits
limit(V > 4.2, error(1))
limit(V < 2.5, error(1))
limit(I > 5, error(1))
limit(I < -5, error(1))

ChgCurrent = battery.oneC
DchCurrent = 1.5

# specify test steps
charge(current=ChgCurrent, voltage=battery.eocVoltage, limits=[I < 0.2])
pause(hours=1, minutes=30)
discharge(current=DchCurrent, limits=[V < battery.eodVoltage])
