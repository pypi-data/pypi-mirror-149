

from .Query import Query
from .utility import check_cols


class Insert(Query):

    def __init__(self, client, structure, columns):
        super().__init__(client=client)

        if columns is None:
            columns = structure.columns

        if len(columns) < 1:
            raise RuntimeError('empty columns')

        if not check_cols(columns, structure.columns):
            raise RuntimeError('invalid columns')

        self.__structure = structure
        self.__columns = columns

    @property
    def structure(self):
        return self.__structure

    @property
    def columns(self):
        return self.__columns
