import bmgen.targets.neware as target
from bmgen.targets.neware.ast import *


class ctrl_for:
    def __init__(self, var: BMVariable, iterable):
        self.var = var
        self.iterable = iterable
        self.simple = isinstance(self.iterable, range) and self.iterable.step == 1
        self.arrayloop = isinstance(self.iterable, BMArray)

    def __enter__(self):
        if self.simple:
            if self.iterable.start != 1:
                target.generator.add(
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
                label = BMLabel(target.generator.label())
                target.generator.add(BMStatement(operator="GOTO", values=[label]))
                target.generator.add(BMStatement(operator="BEG", values=[self.var]))
                target.generator.add(label)
            else:
                target.generator.add(BMStatement(operator="BEG", values=[self.var]))
        elif self.arrayloop:
            counter = BMVariable(self.var.name + "_idx")
            target.generator.add(
                BMStatement(
                    operator="SET",
                    values=[
                        BMAssignment(
                            variable=counter,
                            numvalue=BMNumber(0),
                        )
                    ],
                )
            )
            label = BMLabel(target.generator.label())
            target.generator.add(BMStatement(operator="GOTO", values=[label]))
            target.generator.add(BMStatement(operator="BEG", values=[counter]))
            target.generator.add(label)
            valuevar = self.iterable.__getitem__(counter)
            self.var.name = valuevar.name
        else:
            raise NotImplementedError(
                "BM loops current only work with ranges with stepsize 1 ( e.g. for i in range(10) )"
            )
            pass
        return self.var

    def __exit__(self, type, value, traceback):
        if self.simple:
            target.generator.add(
                BMStatement(
                    operator="CYC",
                    values=[BMCycleCount(BMNumber(self.iterable.stop - 1))],
                )
            )
        elif self.arrayloop:
            target.generator.add(
                BMStatement(
                    operator="CYC",
                    values=[BMCycleCount(BMNumber(self.iterable.arraysize - 1))],
                )
            )
        else:
            # TODO: generic loop
            pass


class ctrl_if:
    def __init__(self, condition: bool, hasElse: bool = False):
        self.condition = condition
        self.hasElse = hasElse

    def __enter__(self):
        if not self.condition:
            self.outer_program = target.generator.program
            target.generator.program = NewareProgram()
        target.generator.context.append(self)

    def __exit__(self, type, value, traceback):
        if not self.condition:
            target.generator.program = self.outer_program
        target.generator.context.remove(self)


class ctrl_else:
    def __init__(self):
        self.if_context = target.generator.context[-1]

    def __enter__(self):
        self.outer_program = target.generator.program
        if self.if_context.condition:
            target.generator.program = NewareProgram()
        else:
            target.generator.program = self.if_context.outer_program

    def __exit__(self, type, value, traceback):
        target.generator.program = self.outer_program
