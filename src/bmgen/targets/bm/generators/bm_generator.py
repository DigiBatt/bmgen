from bmgen.base_generator import BaseGenerator
from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel


class BMGenerator(BaseGenerator):
    def __init__(self):
        self.program = BMProgram()
        self.labelcount = 0

    def finish(self):
        self.add(BMStatement(operator="STO"))
        for i in range(len(self.program.lines)):
            if isinstance(self.program.lines[i], BMLabel):
                label = self.program.lines[i]
                stmt = self.program.lines[i + 1]
                if not isinstance(stmt, BMStatement):
                    raise NotImplementedError("Label must be followed by a statement")
                stmt.label = label.label
                self.program.lines[i] = None

    def add(self, line):
        self.program.lines.append(line)

    def label(self):
        self.labelcount += 1
        return f"bmgen_{self.labelcount}"
