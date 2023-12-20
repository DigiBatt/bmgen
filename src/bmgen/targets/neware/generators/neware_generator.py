from bmgen.base_generator import BaseGenerator
from bmgen.targets.neware.ast import NewareProgram, NewareStatement
import bmgen.targets.neware.constants as constants


class NewareGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.program = NewareProgram()
        self.userVarId = constants.FirstUserVariableId

    def finish(self):
        self.add(NewareStatement(constants.StepType.End))

    def add(self, line):
        self.program.lines.append(line)
        return line

    def ast(self):
        self.finish()
        return str(self.program)

    def userVar(self):
        self.userVarId += 1
        return self.userVarId - 1
