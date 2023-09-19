import bmgen.targets.neware.function as function


def limitcast(limits):
    if not limits:
        return []
    return [__cast(l) for l in limits]


def __cast(l):
    if isinstance(l, function.time):
        return l.toLimit()
    return l
