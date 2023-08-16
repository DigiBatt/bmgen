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

    return c2
