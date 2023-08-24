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
            raise NotImplementedError(
                "BM loops current only work with ranges with stepsize 1 ( e.g. for i in range(10) )"
            )
            pass
        return self.var

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


class ctrl_if:
    def __init__(self, condition: BMLimitCondition, hasElse: bool = False):
        self.condition = condition
        self.baselabel = generator.label()
        self.hasElse = hasElse

    def __enter__(self):
        if self.hasElse:
            notifLabel = self.baselabel + "_else"
        else:
            notifLabel = self.baselabel + "_end"
        generator.add(
            BMStatement(
                operator="PAU",
                limits=[
                    BMLimit(
                        condition=self.condition, action=BMGoto(self.baselabel + "_if")
                    ),
                    BMLimit(
                        condition=BMMultiplication(BMNumber(1), BMVariable("sec")),
                        action=BMGoto(notifLabel),
                    ),
                ],
            )
        )
        generator.add(BMLabel(self.baselabel + "_if"))
        generator.context.append(self)

    def __exit__(self, type, value, traceback):
        generator.add(BMLabel(self.baselabel + "_end"))
        generator.context.remove(self)


class ctrl_else:
    def __init__(self):
        self.baselabel = generator.context[-1].baselabel

    def __enter__(self):
        generator.add(
            BMStatement(operator="GOTO", values=[BMVariable(self.baselabel + "_end")])
        )
        generator.add(BMLabel(self.baselabel + "_else"))

    def __exit__(self, type, value, traceback):
        pass
