import json

from bmgen.targets.python.generators.python_generator import PythonGenerator


class TextGenerator(PythonGenerator):
    def generate(self):
        self.finish()
        return self.program.toText()
