

from .Clause import Clause


class NotBetween(Clause):

    def __init__(self, column, value0, value1):
        super().__init__()

        self.__column = column
        self.__value0 = value0
        self.__value1 = value1

    @property
    def column(self):
        return self.__column

    @property
    def value0(self):
        return self.__value0

    @property
    def value1(self):
        return self.__value1

    def get_not_clause(self):
        from .Between import Between
        return Between(
            column=self.__column,
            value0=self.__value0,
            value1=self.__value1
        )
