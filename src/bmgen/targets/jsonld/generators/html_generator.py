import json

from bmgen.targets.jsonld.generators.jsonld_generator import JSONLDGenerator


class HtmlGenerator(JSONLDGenerator):
    def generate(self):
        self.finish()
        return (
            '<textarea style="width: 100%; height: 100%" readonly>'
            + json.dumps(super().generate().to_jsonld(), indent=2)
            + "</textarea>"
        )
