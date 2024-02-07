# import required functions and channel variables
from bmgen.channel import *
from bmgen.function import *

for idx in range(5):
    pause(seconds=5)

for idx in range(1, 3):
    pause(seconds=5)

values = [2, 1, 5]

for v in values:
    charge(v, limits=[time(seconds=30), V > 4.2])

if len(values) > 2:
    pause(seconds=30)
else:
    pause(seconds=60)

if len(values) < 2:
    pause(seconds=90)
else:
    pause(seconds=120)
