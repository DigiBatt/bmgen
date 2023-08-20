from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel
from bmgen.targets.bm.generators.bm_generator import BMGenerator


class TableGenerator(BMGenerator):
    def generate(self):
        self.finish()
        return self.program.toTable()
