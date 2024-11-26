import json

from bmgen.targets.bcl.generators.bcl_generator import BCLGenerator


class HtmlGenerator(BCLGenerator):
    def generate(self):
        self.finish()
        return (
            '<textarea style="width: 100%; height: 100%" readonly>'
            + json.dumps(self.program.toDict(), indent=2)
            + "</textarea>"
        )
