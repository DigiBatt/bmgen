# import required functions and channel variables
from bmgen.function import *
from bmgen.channel import *

for idx in range(5):
    pause(seconds=5)

for idx in range(1, 3):
    pause(seconds=5)

values = [2, 1, 5]

for v in values:
    charge(v, limits=[time(seconds=30)])
