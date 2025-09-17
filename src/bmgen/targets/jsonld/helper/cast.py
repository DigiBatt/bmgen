import inspect
from functools import wraps
from typing import Dict

import bmgen.targets.bcl.function as function
import bmgen.targets.jsonld.ast as ast


def autocast(**units: str):
    def decorator(f):
        @wraps(f)
        def g(*args, **kwargs):
            params = list(inspect.signature(f).parameters)
            newargs = []
            for a, p in zip(args, params):
                if p in units and a is not None:
                    if isinstance(a, ast.NumericValue):
                        newargs.append(a)
                    else:
                        newargs.append(ast.NumericLiteral(value=a, unit=units[p]))
                else:
                    newargs.append(a)
            args = newargs
            for k, v in kwargs.items():
                if k in units and v is not None:
                    if not isinstance(v, ast.NumericValue):
                        kwargs[k] = ast.NumericLiteral(value=v, unit=units[k])
            return f(*args, **kwargs)

        return g

    return decorator


def limitcast(limits):
    if not limits:
        return []
    return [__cast(l) for l in limits]


def __cast(l):
    if isinstance(l, function.time):
        return l.toLimit()
    return l
