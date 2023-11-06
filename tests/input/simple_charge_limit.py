from bmgen.channel import *
from bmgen.function import *

charge(2.0, voltage=4.2, limits=[time(hours=1), StepCharge > 2.05, I < 0.1])
