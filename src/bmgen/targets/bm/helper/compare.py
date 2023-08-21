def compare(c):
    class c2(c):
        def __lt__(self, other):
            return self.__compare__(other, "<")

        def __gt__(self, other):
            return self.__compare__(other, ">")

        def __le__(self, other):
            return self.__compare__(other, "<=")

        def __ge__(self, other):
            return self.__compare__(other, ">=")

        def __eq__(self, other):
            return self.__compare__(other, "==")

        def __ne__(self, other):
            return self.__compare__(other, "!=")

    c2.__name__ = c.__name__
    c2.__module__ = c.__module__

    return c2
