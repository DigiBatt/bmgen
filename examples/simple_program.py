# from bmgen import battery
from bmgen.function import charge, discharge, pause, time

charge(2.0, voltage=4.2)
# pause(limits=[time(hours=5)])
discharge(1.5)
