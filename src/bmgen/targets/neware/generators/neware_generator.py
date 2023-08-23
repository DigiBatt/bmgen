from bmgen.base_generator import BaseGenerator
from bmgen.targets.neware.ast import NewareProgram, NewareStatement
from bmgen.targets.neware.constants import StepType


class NewareGenerator(BaseGenerator):
    def __init__(self):
        self.program = NewareProgram()

    def finish(self):
        self.add(NewareStatement(StepType.End))

    def add(self, line):
        self.program.lines.append(line)
