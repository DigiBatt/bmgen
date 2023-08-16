from bmgen.targets.bm.ast import BMProgram, BMStatement

x = 3


class Generator:
    def __init__(self):
        self.program = BMProgram()

    def __del__(self):
        print(self.generate())

    def finish(self):
        self.add(BMStatement(operator="STO"))

    def generate(self):
        self.finish()
        return self.program.toTable()

    def add(self, line):
        self.program.lines.append(line)
