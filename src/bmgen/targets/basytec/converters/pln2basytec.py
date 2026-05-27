from bmgen.converter import Converter
from bmgen.targets.bm.formats.sql import Row, StepRows, Program
from bmgen.targets.bm.helper.sql import string_to_sql, list_to_sql
import bmgen.targets.bm.ast as ast
import lark


class LimitTransformer(lark.Transformer):
    def compare(self, values):
        return ast.BMLimitCompare(values[2], values[1], values[0])

    def equals(self, values):
        return ast.BMLimitCompare(values[0], values[1], "=")

    def number(self, values):
        return ast.BMNumber(float(values[0]))

    def identifier(self, values):
        return ast.BMNamedValue(values[0])

    def time(self, values):
        operator = None
        if len(values) == 3:
            operator = str(values[0])
        return ast.BMLimitTime(ast.BMTime(values[0], values[1], operator))

    def OPERATOR(self, value):
        return str(value)

    def IDENTIFIER(self, value):
        return str(value)

    def TIMEUNIT(self, value):
        return str(value)


class SQL2BM(Converter):

    def __init__(self):
        super().__init__()
        self.limitParser = lark.Lark(
            """
            ?limit : equals | compare | time
            equals : value "=" value
            compare : OPERATOR value value
            time: OPERATOR? value TIMEUNIT
            ?value: identifier | number
            identifier: IDENTIFIER
            number: SIGNED_NUMBER
            OPERATOR: /[<>]=?/
            IDENTIFIER: /[a-zA-Z][a-zA-Z0-9_]*/
            TIMEUNIT: /sec|min|h/

            %import common.SIGNED_NUMBER
            %import common.WS
            %ignore WS                     
            """,
            start="limit",
        )

    def convert_Program(self, node: Program):
        return ast.BMProgram([self.convert(r) for r in node.rows])

    def convert_StepRows(self, node: StepRows):
        values = [
            self.convert_value(r.csSetPoint)
            for r in node.rows
            if r.csSetPoint is not None
        ]
        limits = self.convert_limits(node)
        registrations = [
            self.convert_value(r.csRegistration)
            for r in node.rows
            if r.csRegistration is not None
        ]
        return ast.BMStatement(
            node.rows[0].csOperator, values, limits, registrations, node.rows[0].csLabel
        )

    def convert_value(self, value: str):
        if value.endswith(" *"):
            return ast.BMCycleCount(self.convert_value(value[:-2]))
        if " = " in value:
            lhs, rhs = value.split(" = ")
            return ast.BMAssignment(self.convert_value(lhs), self.convert_value(rhs))
        if " " in value:
            lhs, rhs = value.split(" ")
            return ast.BMMultiplication(
                self.convert_value(lhs), self.convert_value(rhs)
            )
        try:
            return ast.BMNumber(float(value))
        except:
            return ast.BMNamedValue(value)

    def convert_limits(self, rows: StepRows):
        limits = []
        limit = None
        combineNext = False
        for r in rows.rows:
            value = r.csCircuitValue
            if value is None:
                continue
            if value.endswith(" &"):
                value = value[:-2]
                combineNext = True
            l = self.convert_limit(value)
            if limit is None:
                limit = l
                action = self.convert_action(r.csBreakOff)
            else:
                limit = ast.BMLimitAnd(limit, l)
            if not combineNext:
                limits.append(ast.BMLimit(limit, action))
                limit = None
        return limits

    def convert_limit(self, limit: str):
        return LimitTransformer().transform(self.limitParser.parse(limit))

    def convert_action(self, action: str | None):
        if action is None:
            return None
        operation, value = action.split(" ")
        match operation:
            case "GOTO":
                return ast.BMGoto(value)
            case "MSG":
                return ast.BMMessage(int(value))
            case "ERR":
                return ast.BMError(int(value))

    def convert_registration(self, registration: str):
        if " " in registration:
            value, channel = registration.split(" ")
            return ast.BMRegCondition(value, channel)
        else:
            return ast.BMRegFormat(registration)
