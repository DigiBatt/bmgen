from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel
from bmgen.targets.bm.generators.bm_generator import BMGenerator


class SqlGenerator(BMGenerator):
    def generate(self):
        self.finish()
        return self.program.toSql(self.programName)
