

from .Query import Query
from .utility import check_cols


class Update(Query):

    def __init__(
            self,
            client,
            structure,
            columns,
            condition):
        super().__init__(client=client)

        if not columns:
            columns = structure.columns

        if not check_cols(columns, structure.columns):
            raise RuntimeError('invalid columns')

        self.__structure = structure
        self.__columns = columns
        self.__condition = condition

    @property
    def structure(self):
        return self.__structure

    @property
    def columns(self):
        return self.__columns

    @property
    def condition(self):
        return self.__condition
