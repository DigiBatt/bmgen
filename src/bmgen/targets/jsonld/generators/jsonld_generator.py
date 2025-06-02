from typing import List

from bmgen.base_generator import BaseGenerator
from bmgen.targets.jsonld.ast import Program, Step


class JSONLDGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = Program([])

    def finish(self):
        pass

    def add(self, step):
        self.program.steps.append(step)
        return step

    def ast(self):
        self.finish()
        return str(self.program)
