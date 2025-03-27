# import required functions and channel variables
import bmgen as bmgen
from bmgen import battery
from bmgen.channel import *
from bmgen.function import *

charge(current=2 * battery.oneC, limits=[I < 0.02 * battery.oneC])
discharge(current=battery.oneC, limits=[I < 0.02 * battery.nominalCapacity])
