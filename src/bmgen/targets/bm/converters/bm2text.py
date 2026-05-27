from bmgen.converter import Converter
from bmgen.targets.bm.formats.sql import Row
import bmgen.targets.bm.ast as ast


class BM2Text(Converter):

    def convert_BMMultiplication(self, node: ast.BMMultiplication):
        return self.convert_node(node.numvalue) + " " + self.convert_node(node.channel)

    def convert_BMCycleCount(self, node: ast.BMCycleCount):
        return self.convert(node.numvalue.toText()) + " *"

    def convert_BMTwoValues(self, node: ast.BMTwoValues):
        return self.convert_node(node.first) + " " + self.convert_node(node.second)

    def convert_BMAssignment(self, node: ast.BMAssignment):
        return self.convert_node(node.variable) + " = " + self.convert_node(node.numvalue)

    def convert_BMNamedValue(self, node: ast.BMNamedValue):
        return node.name

    def convert_BMVariable(self, node: ast.BMVariable):
        return node.name

    def convert_BMChannel(self, node: ast.BMChannel):
        return node.name

    def convert_BMChannelDynamic(self, node: ast.BMChannelDynamic):
        return node.name

    def convert_BMNumber(self, node: ast.BMNumber):
        return str(node.value)

    def convert_BMGoto(self, node: ast.BMGoto):
        return "GOTO " + node.label

    def convert_BMError(self, node: ast.BMError):
        return "ERR " + str(node.errnum)

    def convert_BMMessage(self, node: ast.BMMessage):
        return "MSG " + str(node.errnum)

    def convert_BMLimitCompare(self, node: ast.BMLimitCompare):
        if node.operator == "==":
            return self.convert_node(node.lhs) + " = " + self.convert_node(node.rhs)
        else:
            return node.operator + " " + self.convert_node(node.rhs) + " " + self.convert_node(node.lhs)

    def convert_BMLimitAnd(self, node: ast.BMLimitAnd):
        return self.convert_node(node.lhs) + " &\\r\\n " + self.convert_node(node.rhs)

    def convert_BMTime(self, node: ast.BMTime):
        if node.operator is not None:
            return node.operator + " " + self.convert_node(node.value) + " " + node.unit
        else:
            return self.convert_node(node.value) + " " + node.unit

    def convert_BMLimitTime(self, node: ast.BMLimitTime):
        return self.convert_node(node.time)

    def convert_BMLimit(self, node: ast.BMLimit):
        condition = self.convert_node(node.condition)
        linebreaks = condition.count("\\r\\n")
        action = ""
        if node.action:
            action = "\\r\\n" * linebreaks + self.convert_node(node.action)
        return (condition, action)

    def convert_BMRegCondition(self, node: ast.BMRegCondition):
        return self.convert_node(node.value) + " " + self.convert_node(node.channel)

    def convert_BMRegFormat(self, node: ast.BMRegFormat):
        return node.name

    def convert_BMLabel(self, node: ast.BMLabel):
        return node.label

    def convert_BMStatement(self, node: ast.BMStatement):
        value = "\\r\\n".join([self.convert_node(v) for v in node.values])
        registration = "\\r\\n".join([self.convert_node(r) for r in node.registrations])
        label = node.label if node.label else ""
        if node.limits:
            limit, action = zip(*[self.convert_node(l) for l in node.limits])
        else:
            limit = ""
            action = ""
        limit = "\\r\\n".join(limit)
        action = "\\r\\n".join(action)
        return f"\t{node.__dict__.get('linenumber', '')}\t{label}\t{node.operator}\t{value}\t{limit}\t{action}\t{registration}\n"

    def convert_BMComment(self, node: ast.BMComment):
        return ""

    def convert_BMProgram(self, node: ast.BMProgram):
        program = ""
        linenumber = 1
        for i in range(len(node.lines)):
            line = node.lines[i]
            if not line:
                continue
            if isinstance(line, ast.BMComment):
                program += self.convert_node(line)
            else:
                # Create a copy of the line with linenumber added for conversion
                line_copy = line
                if hasattr(line, 'toText'):
                    program += line.toText(linenumber)
                linenumber += 1
        return program
