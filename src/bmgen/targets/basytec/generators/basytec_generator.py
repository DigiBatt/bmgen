from bmgen.base_generator import BaseGenerator
from bmgen.targets.basytec.ast import BasytecProgram, BasytecStatement
from bmgen.targets.basytec.constants import StepType


class BasytecGenerator(BaseGenerator):
    def __init__(self):
        self.program = BasytecProgram()
        self.stoplabel = False

    def finish(self):
        self.program.lines.insert(
            0, BasytecStatement(StepType.Start, limits=self.program.limits)
        )
        if self.stoplabel:
            label = "STOP"
        else:
            label = None
        self.add(BasytecStatement(StepType.Stop, label=label))

    def add(self, line):
        self.program.lines.append(line)
