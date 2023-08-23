from bmgen.targets.neware.generators.neware_generator import NewareGenerator


class XmlGenerator(NewareGenerator):
    def generate(self):
        return self.program.toXML()
