# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *

register(time=seconds(10), voltage=0.1, current=3.5, format=["eba_fantasy_reg"])

# specify test steps
charge(current=2.0, voltage=4.2, limits=[I < 0.2])
pause(hours=1, minutes=30)
discharge(current=1.5, limits=[V < 3.0])
