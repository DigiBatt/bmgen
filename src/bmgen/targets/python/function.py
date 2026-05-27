from dataclasses import dataclass
from typing import Any, List

import bmgen.targets.python as target
import bmgen.targets.python.ast as ast
import bmgen.targets.python.channel as channel


def charge(*args, **kwargs):
    return target.generator.add(ast.FunctionCall("charge", args, kwargs))


def discharge(*args, **kwargs):
    return target.generator.add(ast.FunctionCall("discharge", args, kwargs))


def pause(*args, **kwargs):
    return target.generator.add(ast.FunctionCall("pause", args, kwargs))


def time(
    hours: ast.NumericExpression | None = None,
    minutes: ast.NumericExpression | None = None,
    seconds: ast.NumericExpression | None = None,
):
    return ast.TimeExpression(hours, minutes, seconds)


def seconds(value: float):
    return time(None, None, value)


def minutes(value: float) -> time:
    return time(None, value, None)


def hours(value: float) -> time:
    return time(value, None, None)


def limit(*args, **kwargs):
    return ast.FunctionCall("limit", args, kwargs)


def limit_global(*args, **kwargs):
    return target.generator.add(ast.FunctionCall("limit", args, kwargs))


def error(*args, **kwargs):
    return ast.FunctionCall("error", args, kwargs)


def register(*args, **kwargs):
    return ast.FunctionCall("register", args, kwargs)


def register_global(*args, **kwargs):
    return target.generator.add(ast.FunctionCall("register", args, kwargs))


def constant(value):
    return ast.NumberLiteral(value)
