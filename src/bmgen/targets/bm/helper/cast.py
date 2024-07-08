import inspect
from functools import wraps
from typing import List

import bmgen.targets.bm.ast as ast
from bmgen.targets.bm.time import time


def cast_literal(x):
    if isinstance(x, (float, int)):
        return ast.BMNumber(x)
    elif isinstance(x, str):
        return ast.BMVariable(x)
    elif isinstance(x, ast.BMLimitCondition):
        return ast.BMLimit(x)
    elif isinstance(x, list):
        return [cast_literal(y) for y in x]
    elif isinstance(x, time):
        return x.toLimit()
    else:
        return x


def autocast(names: str | List[str] | None = None):
    if isinstance(names, str):
        names = [names]

    def decorator(f):
        @wraps(f)
        def g(*args, **kwargs):
            if names:
                params = list(inspect.signature(f).parameters)
                newargs = []
                for a, p in zip(args, params):
                    if p in names:
                        newargs.append(cast_literal(a))
                    else:
                        newargs.append(a)
                args = newargs
                for k, v in kwargs.items():
                    if k in names:
                        kwargs[k] = cast_literal(v)
            else:
                args = [cast_literal(x) for x in args]
                kwargs = {k: cast_literal(v) for k, v in kwargs.items()}
            return f(*args, **kwargs)

        return g

    return decorator
