from bmgen.converter import Converter
from bmgen.targets.bm.formats.sql import Row, StepRows, Program
from bmgen.targets.bm.helper.sql import string_to_sql, list_to_sql
import bmgen.targets.bm.ast as ast
from bmgen.targets.bm.converters.bm2text import BM2Text


class BM2SQL(Converter):

    def __init__(self):
        self.fallback = BM2Text()

    def convert_BMLimitAnd(self, node: ast.BMLimitAnd):
        lhs = self.convert_node(lhs)
        if isinstance(lhs, str):
            lhs = [lhs]
        rhs = self.convert_node(rhs)
        if isinstance(rhs, str):
            rhs = [rhs]
        lhs[-1] += " &"
        return [*lhs, *rhs]

    def convert_BMLimitCompare(self, node: ast.BMLimitCompare):
        if node.operator == "==":
            return [self.convert_node(node.lhs) + " = " + self.convert_node(node.rhs)]
        else:
            return [
                node.operator
                + " "
                + self.convert_node(node.rhs)
                + " "
                + self.convert_node(node.lhs)
            ]

    def convert_BMLimitTime(self, node: ast.BMLimitTime):
        return [self.convert_node(node.time)]

    def convert_BMStatement(self, node: ast.BMStatement):
        rows = []
        nRows = max(len(node.values), len(node.limits), len(node.registrations), 1)
        iNumeration = 0
        for iRow in range(nRows):
            label = None
            operator = None
            action = None
            limit = [None]
            value = self.__get_index_converted(node.values, iRow)
            if iNumeration == 0:
                label = node.label
                operator = node.operator
            if len(node.limits) > iRow:
                limit = self.convert_node(node.limits[iRow].condition)
                if node.limits[iRow].action is not None:
                    action = self.convert_node(node.limits[iRow].action)
            registration = self.__get_index_converted(node.registrations, iRow)
            for iLimit in range(len(limit)):
                rows.append(
                    Row(
                        None,
                        iNumeration,
                        label,
                        operator,
                        value,
                        limit[iLimit],
                        action,
                        registration,
                        None,
                        None,
                    )
                )
                label = None
                operator = None
                value = None
                action = None
                registration = None
                iNumeration += 1

        return StepRows(rows)

    def convert_BMProgram(self, node: ast.BMProgram):
        rows = []
        iStep = 1
        for line in node.lines:
            if not line:
                continue
            stepRows = self.convert_node(line)
            for row in stepRows.rows:
                row.iStepNo = iStep
            rows.append(stepRows)
            iStep += 1
        return Program(rows)

    def __get_index_converted(self, values, idx):
        if len(values) > idx:
            return self.convert_node(values[idx])
        else:
            return None
