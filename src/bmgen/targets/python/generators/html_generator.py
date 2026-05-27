import json

from bmgen.targets.python.generators.python_generator import PythonGenerator


class HtmlGenerator(PythonGenerator):
    def generate(self):
        self.finish()
        return (
            '<textarea style="width: 100%; height: 100%" readonly>'
            + self.program.toText()
            + "</textarea>"
        )
