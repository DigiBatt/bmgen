import bmgen.targets.basytec.ast as ast
from typing import Dict
import inspect
from functools import wraps


def autocast(**units: Dict[str, str]):
    def decorator(f):
        @wraps(f)
        def g(*args, **kwargs):
            params = list(inspect.signature(f).parameters)
            newargs = []
            for a, p in zip(args, params):
                if p in units:
                    newargs.append(
                        ast.BasytecValue(value=a, unit=ast.BasytecUnit(units[p]))
                    )
                else:
                    newargs.append(a)
            args = newargs
            for k, v in kwargs.items():
                if k in units:
                    kwargs[k] = ast.BasytecValue(
                        value=v, unit=ast.BasytecUnit(units[k])
                    )
            return f(*args, **kwargs)

        return g

    return decorator
