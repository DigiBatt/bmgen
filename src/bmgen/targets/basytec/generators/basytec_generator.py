from bmgen.base_generator import BaseGenerator
from bmgen.targets.basytec.ast import BasytecProgram, BasytecStatement, BasytecSetValue
from bmgen.targets.basytec.constants import StepType
from typing import List


class BasytecGenerator(BaseGenerator):
    def __init__(self):
        self.program = BasytecProgram()
        self.stoplabel = False
        self.registrations: List[BasytecSetValue] = []

    def finish(self):
        self.program.lines.insert(
            0, BasytecStatement(StepType.Start, limits=self.program.limits)
        )
        if self.stoplabel:
            label = "STOP"
        else:
            label = None
        self.program.lines.append(BasytecStatement(StepType.Stop, label=label))

    def add(self, line):
        if not line.registrations:
            line.registrations = self.registrations
        self.program.lines.append(line)
        return line

    def set_registration(self, registrations: List[BasytecSetValue]):
        self.registrations = registrations

    def ast(self):
        self.finish()
        return str(self.program)
