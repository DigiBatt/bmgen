import bmgen.targets.bm as target
import bmgen.targets.bm.function as function
from bmgen.targets.bm.ast import *
from bmgen.targets.bm.helper.cast import cast_literal
from bmgen.targets.bm.program import variable


def ctrl_for(iterable, body, var, g, l):
    if not isinstance(var, BMVariable):
        var = variable(var)
    simple = isinstance(iterable, function.BMRange) and iterable.step == 1
    if not simple and isinstance(iterable, (function.BMRange, list)):
        iterable = variable(var.name + "_arr", iterable)
    arrayloop = isinstance(iterable, BMArray)
    code = compile(body, "<bmgen_loop>", "exec")
    if simple:
        if iterable.start != 1:
            target.generator.add(
                BMStatement(
                    operator="SET",
                    values=[
                        BMAssignment(
                            variable=var,
                            numvalue=cast_literal(iterable.start),
                        )
                    ],
                )
            )
        cyclecount = cast_literal(iterable.stop - 1)
        if iterable.start != 1:
            label = BMLabel(target.generator.label())
            target.generator.add(BMStatement(operator="GOTO", values=[label]))
            target.generator.add(BMStatement(operator="BEG", values=[var]))
            target.generator.add(label)
        else:
            target.generator.add(BMStatement(operator="BEG", values=[var]))
        l[var.name] = var
        exec(code, g, l)
        target.generator.add(
            BMStatement(
                operator="CYC",
                values=[BMCycleCount(cyclecount)],
            )
        )
    elif arrayloop:
        counter = BMVariable(var.name + "_idx")
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
        valuevar = iterable.__getitem__(counter)
        l[var.name] = valuevar
        var.name = valuevar.name
        exec(code, g, l)
        target.generator.add(
            BMStatement(
                operator="CYC",
                values=[BMCycleCount(BMNumber(iterable.arraysize - 1))],
            )
        )
    else:
        try:
            iterable = iterable.to_python_range()
        except:
            # raise Exception("Cannot process iterable in for loop")
            pass
        for i in iterable:
            l[var.name] = i
            exec(code, g, l)


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
        target.generator.context.remove(self)
        if isinstance(self.condition, bool):
            target.generator.unfreeze()
            return

        target.generator.add(BMLabel(self.baselabel + "_end"))


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
        if isinstance(condition, bool):
            target.generator.unfreeze()
