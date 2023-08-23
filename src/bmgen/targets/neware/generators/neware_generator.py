from bmgen.base_generator import BaseGenerator
from bmgen.targets.neware.ast import NewareProgram


class NewareGenerator(BaseGenerator):
    def __init__(self):
        self.program = NewareProgram()

    def add(self, line):
        self.program.lines.append(line)
