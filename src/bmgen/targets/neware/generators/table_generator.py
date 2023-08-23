from bmgen.targets.neware.generators.neware_generator import NewareGenerator


class TableGenerator(NewareGenerator):
    def generate(self):
        self.finish()
        return self.program.toTable()
