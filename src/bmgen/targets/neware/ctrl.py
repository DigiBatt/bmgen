import bmgen.targets.neware as target
from bmgen.targets.neware.ast import NewareCycleCount, NewareStartStep, NewareStatement
from bmgen.targets.neware.constants import StepType


def ctrl_for(iterable, body, var, g, l):
    simple = isinstance(iterable, range) and iterable.step == 1
    code = compile(body, "<bmgen_loop>", "exec")
    if simple:
        start_step = len(target.generator.program.lines) + 1
        cycle_count = iterable.stop - iterable.start
        exec(code, g, l)
        target.generator.add(
            NewareStatement(
                StepType.Cycle,
                others=[
                    NewareStartStep(start_step),
                    NewareCycleCount(cycle_count),
                ],
            )
        )
    else:
        for i in iterable:
            l[var] = i
            exec(code, g, l)
