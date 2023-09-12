# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *

# set safety limits
limit(V > 4.2, error(1))
limit(V < 2.5, error(1))
limit(I > 5, error(1))
limit(I < -5, error(1))

ChgCurrent = 2.0
DchCurrent = 1.5

# specify test steps
charge(current=ChgCurrent, voltage=4.2, limits=[I < 0.2])
pause(hours=1, minutes=30)
discharge(current=DchCurrent, limits=[V < 3.0])
