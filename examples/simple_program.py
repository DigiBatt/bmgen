# from bmgen import battery
from bmgen.function import charge, discharge, pause, time, limit, error
from bmgen.channel import I, V

limit(V > 4.3, error(1))

charge(2.0, voltage=4.2, limits=[I < 0.2])
pause(limits=[time(hours=5)])
discharge(1.5, limits=[V < 3.0])
