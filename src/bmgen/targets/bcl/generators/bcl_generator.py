from typing import List

from bmgen.base_generator import BaseGenerator
from bmgen.targets.bcl.ast import BCLInstruction, BCLProgram


class BCLGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = BCLProgram("program", {}, [])

    def finish(self):
        pass

    def add(self, step):
        if len(self.program.instructions) == 0:
            self.program.instructions.append(BCLInstruction([], 1))
        self.program.instructions[-1].sequence.append(step)
        return step

    def ast(self):
        self.finish()
        return str(self.program)
