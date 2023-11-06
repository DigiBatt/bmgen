from bmgen.function import *
from bmgen.channel import *

dV = channel("dV")

charge(2.0, limits=[dV < 0.02])
