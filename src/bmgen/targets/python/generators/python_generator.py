from bmgen.base_generator import BaseGenerator
import bmgen.targets.python.ast as ast


class PythonGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = ast.Program()

    def finish(self):
        pass

    def add(self, step):
        self.program.statements.append(step)
        return step

    def ast(self):
        self.finish()
        return self.program.toText()
