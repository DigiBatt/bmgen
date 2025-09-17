import json

from bmgen.targets.jsonld.generators.jsonld_generator import JSONLDGenerator


class JsonGenerator(JSONLDGenerator):
    def generate(self):
        return json.dumps(super().generate().to_jsonld(), indent=2)
