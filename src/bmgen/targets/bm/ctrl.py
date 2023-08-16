from bmgen.targets.bm import generator
from bmgen.targets.bm.ast import *


class ctrl_for:
    def __init__(self, var: BMVariable, iterable):
        self.var = var
        self.iterable = iterable
        self.simple = isinstance(self.iterable, range) and self.iterable.step == 1

    def __enter__(self):
        if self.simple:
            if self.iterable.start != 0:
                generator.add(
                    BMStatement(
                        operator="SET",
                        values=[
                            BMAssignment(
                                variable=self.var,
                                numvalue=BMNumber(self.iterable.start),
                            )
                        ],
                    )
                )
            generator.add(BMStatement(operator="BEG", values=[self.var]))
        else:
            # TODO: generic loop
            pass

    def __exit__(self, type, value, traceback):
        if self.simple:
            generator.add(
                BMStatement(
                    operator="CYC", values=[BMCycleCount(BMNumber(self.iterable.stop))]
                )
            )
        else:
            # TODO: generic loop
            pass
