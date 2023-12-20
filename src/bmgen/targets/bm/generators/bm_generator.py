from bmgen.base_generator import BaseGenerator
from bmgen.targets.bm.ast import (
    BMProgram,
    BMStatement,
    BMLabel,
    BMMultiplication,
    BMNumber,
    BMVariable,
)
import bmgen


class BMGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = BMProgram()
        self.labelcount = 0
        self.arraycount = 0

    def finish(self):
        # add stop line
        self.add(BMStatement(operator="STO"))

        if bmgen.options.get("bm", {}).get("safetask", False):
            self.program.lines.insert(
                0,
                BMStatement(
                    operator="TASK",
                    values=[BMMultiplication(BMNumber(1), BMVariable("SafeTask"))],
                ),
            )

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
        next_line = None
        for i in range(len(self.program.lines) - 1, -1, -1):
            curr_set_value = False
            curr_set_limit = False
            line = self.program.lines[i]
            if i < len(self.program.lines) - 1:
                next_line = self.program.lines[i + 1]
            if not line:
                continue
            if line.operator == "SET":
                if line.values and not line.limits:
                    if (
                        prev_set_value
                        and (len(line.values) + len(next_line.values)) <= 10
                    ):
                        line.values += next_line.values
                        self.program.lines[i + 1] = None
                    if not line.label:
                        curr_set_value = True
                elif line.limits and not line.values:
                    if (
                        prev_set_limit
                        and (len(line.limits) + len(next_line.limits)) <= 10
                    ):
                        line.limits += next_line.limits
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

    def ast(self):
        self.finish()
        return str(self.program)
