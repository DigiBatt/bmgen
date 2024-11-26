import json

from bmgen.targets.bcl.generators.bcl_generator import BCLGenerator
from bmgen.targets.bcl.helper.convertToJsonld import convert_to_json_ld


class JsonldGenerator(BCLGenerator):
    def generate(self):
        self.finish()
        return json.dumps(convert_to_json_ld(self.program.toDict()), indent=2)
