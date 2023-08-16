from bmgen.targets.bm.ast import BMNumber, BMVariable, BMLimit, BMLimitCondition


def cast_literal(x):
    if isinstance(x, (float, int)):
        return BMNumber(x)
    elif isinstance(x, str):
        return BMVariable(x)
    elif isinstance(x, BMLimitCondition):
        return BMLimit(x)
    elif isinstance(x, list):
        return [cast_literal(y) for y in x]
    else:
        return x


def autocast(f):
    def g(*args, **kwargs):
        args = [cast_literal(x) for x in args]
        kwargs = {k: cast_literal(v) for k, v in kwargs.items()}
        return f(*args, **kwargs)

    return g
