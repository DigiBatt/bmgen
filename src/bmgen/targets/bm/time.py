import bmgen.targets.bm.ast as ast
import typing
from dataclasses import dataclass


@dataclass
class time:
    hours: typing.Union["ast.BMNumValue", None] = None
    minutes: typing.Union["ast.BMNumValue", None] = None
    seconds: typing.Union["ast.BMNumValue", None] = None

    def toLimit(self) -> "ast.BMLimit":
        return ast.BMLimit(ast.BMLimitTime(self.toBMTime()))

    def toBMTime(self) -> "ast.BMTime":
        if self.seconds:
            if self.hours:
                if isinstance(self.hours, ast.BMNumber) and isinstance(
                    self.seconds, ast.BMNumber
                ):
                    self.seconds.value += self.hours.value * 3600
                else:
                    raise NotImplementedError("BM time limit can only have one unit")
            if self.minutes:
                if isinstance(self.minutes, ast.BMNumber) and isinstance(
                    self.seconds, ast.BMNumber
                ):
                    self.seconds.value += self.minutes.value * 60
                else:
                    raise NotImplementedError("BM time limit can only have one unit")
            return ast.BMTime(value=self.seconds, unit="s")
        if self.minutes:
            if self.hours:
                if isinstance(self.hours, ast.BMNumber) and isinstance(
                    self.minutes, ast.BMNumber
                ):
                    self.minutes.value += self.hours.value * 60
                else:
                    raise NotImplementedError("BM time limit can only have one unit")
            return ast.BMTime(value=self.minutes, unit="min")
        if self.hours:
            return ast.BMTime(value=self.hours, unit="h")
