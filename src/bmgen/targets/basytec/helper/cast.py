import bmgen.targets.basytec.ast as ast
from typing import Dict
import inspect
from functools import wraps
import bmgen.targets.basytec.function as function


def autocast(**units: Dict[str, str]):
    def decorator(f):
        @wraps(f)
        def g(*args, **kwargs):
            params = list(inspect.signature(f).parameters)
            newargs = []
            for a, p in zip(args, params):
                if p in units and a is not None:
                    if isinstance(a, ast.BasytecValue):
                        newargs.append(a)
                    else:
                        newargs.append(
                            ast.BasytecValueLiteral(
                                value=a, unit=ast.BasytecUnit(units[p])
                            )
                        )
                else:
                    newargs.append(a)
            args = newargs
            for k, v in kwargs.items():
                if k in units and v is not None:
                    if not isinstance(v, ast.BasytecValue):
                        kwargs[k] = ast.BasytecValueLiteral(
                            value=v, unit=ast.BasytecUnit(units[k])
                        )
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
