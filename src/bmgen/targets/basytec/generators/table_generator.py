from bmgen.targets.basytec.generators.basytec_generator import BasytecGenerator


class TableGenerator(BasytecGenerator):
    def generate(self):
        self.finish()
        return self.program.toTable()
