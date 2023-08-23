from bmgen.targets.basytec.generators.basytec_generator import BasytecGenerator


class TextGenerator(BasytecGenerator):
    def generate(self):
        self.finish()
        program = self.program.toText().encode()
        program = program.replace(b"\xc3\xbe\xc3\xbd", b"\xfe\xfd")
        return program
