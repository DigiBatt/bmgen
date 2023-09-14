from bmgen.base_generator import BaseGenerator
from bmgen.targets.bm.ast import BMProgram, BMStatement, BMLabel


class BMGenerator(BaseGenerator):
    def __init__(self):
        self.program = BMProgram()
        self.labelcount = 0
        self.arraycount = 0
        self.context = []

    def finish(self):
        # add stop line
        self.add(BMStatement(operator="STO"))

        # combine labels with next line
        for i in range(len(self.program.lines)):
            if isinstance(self.program.lines[i], BMLabel):
                label = self.program.lines[i]
                stmt = self.program.lines[i + 1]
                if not isinstance(stmt, BMStatement):
                    raise NotImplementedError("Label must be followed by a statement")
                stmt.label = label.label
                self.program.lines[i] = None

        # combine SET statements
        prev_set_value = False
        prev_set_limit = False
        for i in range(len(self.program.lines) - 1, -1, -1):
            curr_set_value = False
            curr_set_limit = False
            line = self.program.lines[i]
            if not line:
                continue
            if line.operator == "SET":
                if line.values and not line.limits:
                    if prev_set_value:
                        line.values += self.program.lines[i + 1].values
                        self.program.lines[i + 1] = None
                    if not line.label:
                        curr_set_value = True
                elif line.limits and not line.values:
                    if prev_set_limit:
                        line.limits += self.program.lines[i + 1].limits
                        self.program.lines[i + 1] = None
                    if not line.label:
                        curr_set_limit = True
            prev_set_value = curr_set_value
            prev_set_limit = curr_set_limit

    def add(self, line):
        self.program.lines.append(line)
        return line

    def label(self):
        self.labelcount += 1
        return f"bmgen_{self.labelcount}"

    def array(self):
        self.arraycount += 1
        return self.arraycount - 1
