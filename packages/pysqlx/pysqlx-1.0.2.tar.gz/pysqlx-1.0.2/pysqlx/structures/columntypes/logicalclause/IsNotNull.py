

from .Clause import Clause


class IsNotNull(Clause):

    def __init__(self, column):
        super().__init__()

        self.__column = column

    @property
    def column(self):
        return self.__column

    def get_not_clause(self):
        from .IsNull import IsNull
        return IsNull(column=self.__column)
