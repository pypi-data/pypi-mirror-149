

from .Clause import Clause


class And(Clause):

    def __init__(self, clause0, clause1):

        if not all((
            isinstance(clause0, Clause),
            isinstance(clause1, Clause),
        )):
            raise RuntimeError(
                'invalid clauses of types "%s" and "%s"' % (
                    type(clause0).__name__,
                    type(clause1).__name__,
                )
            )

        super().__init__()

        self.__clause0 = clause0
        self.__clause1 = clause1

    @property
    def clause0(self):
        return self.__clause0

    @property
    def clause1(self):
        return self.__clause1

    def get_not_clause(self):
        from .Or import Or
        return Or(
            clause0=self.__clause0.get_not_clause(),
            clause1=self.__clause1.get_not_clause()
        )
