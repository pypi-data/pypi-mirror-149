

from .Clause import Clause


class NotInList(Clause):

    def __init__(self, column, val_list):
        super().__init__()

        self.__column = column
        self.__val_list = val_list

    @property
    def column(self):
        return self.__column

    @property
    def val_list(self):
        return self.__val_list

    def get_not_clause(self):
        from .InList import InList
        return InList(column=self.__column, val_list=self.__val_list)
