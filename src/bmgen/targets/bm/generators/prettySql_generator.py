from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel
from bmgen.targets.bm.generators.sql_generator import SqlGenerator


class PrettysqlGenerator(SqlGenerator):
    def generate(self):
        return super().generate().replace("\n", "<br>")
