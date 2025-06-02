# import required functions and channel variables
from bmgen.channel import *
from bmgen.function import *

# set safety limits
# limit(V > 4.2, error(1))
# limit(V < 2.5, error(1))
# limit(I > 5, error(1))
# limit(I < -5, error(1))

# specify test steps
charge(current=2.0, voltage=4.2, limits=[I < 0.2])
# pause(hours=1, minutes=30)
# discharge(current=1.5, limits=[V < 3.0])
