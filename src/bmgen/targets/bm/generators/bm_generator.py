import bmgen
from bmgen.base_generator import BaseGenerator
from bmgen.targets.bm.ast import (
    BMAssignment,
    BMLabel,
    BMMultiplication,
    BMNamedValue,
    BMNumber,
    BMNumValue,
    BMProgram,
    BMStatement,
    BMVariable,
)


class BMGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = BMProgram()
        self.labelcount = 0
        self.arraycount = 0
        self.tempcount = 0
        self.frozen = False

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

        modified = True
        while modified:
            modified = False

            # combine labels with next line
            for i in range(len(self.program.lines)):
                if isinstance(self.program.lines[i], BMLabel):
                    label = self.program.lines[i]
                    stmt = self.program.lines[i + 1]
                    if not isinstance(stmt, BMStatement):
                        raise NotImplementedError(
                            "Label must be followed by a statement"
                        )
                    stmt.label = label.label
                    self.program.lines[i] = None
                    modified = True

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
                            modified = True
                        if not line.label:
                            curr_set_value = True
                    elif line.limits and not line.values:
                        if (
                            prev_set_limit
                            and (len(line.limits) + len(next_line.limits)) <= 10
                        ):
                            line.limits += next_line.limits
                            self.program.lines[i + 1] = None
                            modified = True
                        if not line.label:
                            curr_set_limit = True
                prev_set_value = curr_set_value
                prev_set_limit = curr_set_limit

            # remove unnecessary temporary variables and calculations
            for i in range(len(self.program.lines) - 3, -1, -1):
                match self.program.lines[i : i + 3]:
                    case [
                        BMStatement(
                            "SET",
                            [
                                *vals1,
                                BMAssignment(
                                    BMNamedValue(), BMNamedValue(lhs1)
                                ) as assign1,
                            ],
                        ),
                        BMStatement(
                            "ADD" | "SUB" | "DIV" | "MUL",
                            [BMNamedValue(var), BMNumValue()],
                        ) as calc,
                        BMStatement(
                            "SET",
                            [
                                BMAssignment(
                                    BMNamedValue(rhs2), BMNamedValue()
                                ) as assign2,
                                *vals2,
                            ],
                        ) as set2,
                    ] if var.startswith("bmgen_") and lhs1 == var and rhs2 == var:
                        assign1.variable = assign2.variable
                        calc.values[0] = assign2.variable
                        if len(set2.values) > 1:
                            set2.values = set2.values[1:]
                        else:
                            self.program.lines[i + 2] = None
                        modified = True
                    case [
                        BMStatement(
                            "ADD" | "SUB" as op1, [BMNamedValue(var1), BMNumber(val1)]
                        ),
                        BMStatement(
                            "ADD" | "SUB" as op2, [BMNamedValue(var2), BMNumber(val2)]
                        ),
                        _,
                    ] if op1 != op2 and var1 == var2 and val1 == val2:
                        self.program.lines[i] = None
                        self.program.lines[i + 1] = None
                        modified = True

            self.program.lines = [
                line for line in self.program.lines if line is not None
            ]

    def add(self, line):
        if not self.frozen:
            self.program.lines.append(line)
        return line

    def label(self):
        if not self.frozen:
            self.labelcount += 1
        return f"bmgen_{self.labelcount}"

    def array(self):
        if not self.frozen:
            self.arraycount += 1
        return self.arraycount - 1

    def ast(self):
        self.finish()
        return str(self.program)

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False
