

from .Clause import Clause


class NotEqual(Clause):

    def __init__(self, lhs, rhs):
        super().__init__()

        self.__lhs = lhs
        self.__rhs = rhs

    @property
    def lhs(self):
        return self.__lhs

    @property
    def rhs(self):
        return self.__rhs

    def get_not_clause(self):
        from .Equal import Equal
        return Equal(lhs=self.lhs, rhs=self.rhs)
