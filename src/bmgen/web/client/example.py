# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *

# set data recording interval
# registration format is only applied to BM programs
register(time=seconds(1), format=["my_custom_reg"])

# set safety limits
limit(V > 4.2, error(1))
limit(V < 2.5, error(1))
limit(I > 5, error(1))
limit(I < -5, error(1))

# specify test steps
charge(current=2.0, voltage=4.2, limits=[I < 0.2])
pause(hours=1, minutes=30)
discharge(current=1.5, limits=[V < 3.0])
