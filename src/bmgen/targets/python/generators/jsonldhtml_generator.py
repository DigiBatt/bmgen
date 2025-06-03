import json

from bmgen.targets.bcl.generators.bcl_generator import BCLGenerator
from bmgen.targets.bcl.helper.convertToJsonld import convert_to_json_ld


class JsonldhtmlGenerator(BCLGenerator):
    def generate(self):
        self.finish()
        return (
            '<textarea style="width: 100%; height: 100%" readonly>'
            + json.dumps(convert_to_json_ld(self.program.toDict()), indent=2)
            + "</textarea>"
        )
