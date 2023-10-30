from bmgen.function import charge
from bmgen.channel import V

test = 5
test += 3
test -= 7
test *= 3
test /= 2
charge(test, limits=[V > 4.2])
