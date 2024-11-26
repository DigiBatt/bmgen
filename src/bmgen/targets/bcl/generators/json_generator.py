import json

from bmgen.targets.bcl.generators.bcl_generator import BCLGenerator


class JsonGenerator(BCLGenerator):
    def generate(self):
        self.finish()
        return json.dumps(self.program.toDict(), indent=2)
