import bmgen.targets.bm as target
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.program import variable


class ctrl_for:
    def __init__(self, var: BMVariable, iterable):
        if isinstance(iterable, list):
            iterable = variable(var.name + "_arr", iterable)
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
                "BM loops currently only work with ranges with stepsize 1 ( e.g. for i in range(10) )"
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
    def __init__(self, condition: BMLimitCondition, hasElse: bool = False):
        self.condition = condition
        self.baselabel = target.generator.label()
        self.hasElse = hasElse

    def __enter__(self):
        target.generator.context.append(self)

        if isinstance(
            self.condition, bool
        ):  # condition evaluated at compile time -> only run one branch of if/else
            if not self.condition:
                target.generator.freeze()
            return

        if self.hasElse:
            notifLabel = self.baselabel + "_else"
        else:
            notifLabel = self.baselabel + "_end"
        target.generator.add(
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
        target.generator.add(BMLabel(self.baselabel + "_if"))

    def __exit__(self, type, value, traceback):
        if isinstance(self.condition, bool):
            return

        target.generator.add(BMLabel(self.baselabel + "_end"))
        target.generator.context.remove(self)


class ctrl_else:
    def __init__(self):
        self.baselabel = target.generator.context[-1].baselabel

    def __enter__(self):
        condition = target.generator.context[-1].condition
        if isinstance(condition, bool):
            if condition:
                target.generator.freeze()
            else:
                target.generator.unfreeze()
            return

        target.generator.add(
            BMStatement(operator="GOTO", values=[BMVariable(self.baselabel + "_end")])
        )
        target.generator.add(BMLabel(self.baselabel + "_else"))

    def __exit__(self, type, value, traceback):
        condition = target.generator.context[-1].condition
        if isinstance(condition, bool) and condition == True:
            target.generator.unfreeze()
