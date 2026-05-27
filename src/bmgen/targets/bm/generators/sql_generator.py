from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel
from bmgen.targets.bm.generators.bm_generator import BMGenerator
from bmgen.targets.bm.converters.bm2sql import BM2SQL


class SqlGenerator(BMGenerator):
    def generate(self):
        self.finish()
        converter = BM2SQL()
        program = converter.convert(self.program)
        return program.toSql(self.programName)
