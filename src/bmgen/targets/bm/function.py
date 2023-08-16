from bmgen.targets.bm import generator
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.helper.cast import autocast
from typing import List


@autocast
def charge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] = [],
):
    if isinstance(current, BMNumValue):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, "V"))

    generator.add(BMStatement(operator="CHA", values=[current], limits=limits))


@autocast
def discharge(
    current: BMNumValue | BMMultiplication,
    voltage: BMNumValue | None = None,
    limits: List[BMLimit] = [],
):
    if isinstance(current, BMNumValue):
        current = BMMultiplication(current, BMVariable("A"))
    values = [current]
    if voltage:
        values.append(BMMultiplication(voltage, "V"))

    generator.add(BMStatement(operator="DCH", values=[current], limits=limits))
