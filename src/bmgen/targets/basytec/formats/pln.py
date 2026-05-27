import typing
from dataclasses import dataclass
import lark


@dataclass
class Header:
    registrations: typing.List[str]
    numRows: int
    numColumns: int


@dataclass
class Row:
    stepnumber: int
    label: str | None
    command: str
    parameters: typing.List[str]
    terminations: typing.List[str]
    actions: typing.List[str]
    registrations: typing.List[str]


@dataclass
class Program:
    header: Header
    rows: typing.List[Row]

    @staticmethod
    def fromPln(buffer):
        parser = lark.Lark(
            r"""
            program : header steplist
            header: headername reglength headerreg* programlength
            steplist: step*
            headername: VALUE LB
            reglength: NUMBER LB
            headerreg: VALUE LB
            programlength: NUMBER NUMBER LB
            step: stepnumber level label command parameter termination action registration comment
            stepnumber: "0" NUMBER VALUE? LB
            level: "1" NUMBER VALUE? LB
            label: "2" NUMBER VALUE? LB
            command: "3" NUMBER VALUE? LB
            parameter: "4" NUMBER VALUE? LB
            termination: "5" NUMBER VALUE? LB
            action: "6" NUMBER VALUE? LB
            registration: "7" NUMBER VALUE? LB
            comment: "8" NUMBER VALUE? LB

            VALUE: /([a-zA-Z0-9_<>+-.]|\xef|\xbf|\xbd|\[|\])+/
            SPACE: / +/
            NUMBER: /[0-9]+/
            LB: /\n/

            %ignore SPACE                     
        """,
            start="program",
            use_bytes=True,
        )
        tree = parser.parse(buffer.read())
        print(tree.pretty())
        # buffer.readline()
        # nRegistrations = int(buffer.readline())
        # registrations = [buffer.readline() for _ in range(nRegistrations)]
        # programLength = buffer.readline()
        # numSteps = int(programLength.strip().split(" ")[1])
        # steps = [Row.fromPln(buffer) for _ in range(numSteps)]
