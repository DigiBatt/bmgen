def string_to_sql(s):
    if s is None:
        return "null"
    elif s.startswith("'") and s.endswith("'"):
        return s
    else:
        return "'" + s + "'"


def list_to_sql(a, i):
    if len(a) <= i or a[i] is None:
        return "null"
    else:
        return a[i].toSql()
