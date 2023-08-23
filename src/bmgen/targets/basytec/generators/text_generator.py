from bmgen.targets.basytec.generators.basytec_generator import BasytecGenerator


class TextGenerator(BasytecGenerator):
    def generate(self):
        self.finish()
        return self.program.toText()
