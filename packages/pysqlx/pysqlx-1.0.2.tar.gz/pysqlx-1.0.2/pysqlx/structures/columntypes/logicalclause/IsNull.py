

from .Clause import Clause


class IsNull(Clause):

    def __init__(self, column):
        super().__init__()

        self.__column = column

    @property
    def column(self):
        return self.__column

    def get_not_clause(self):
        from .IsNotNull import IsNotNull
        return IsNotNull(column=self.__column)
