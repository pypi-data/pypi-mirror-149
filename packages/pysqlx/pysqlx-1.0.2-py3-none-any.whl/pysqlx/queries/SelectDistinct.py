

from .Query import Query
from .utility import check_cols, check_order_by_cols


class SelectDistinct(Query):

    def __init__(
            self,
            client,
            structure,
            columns,
            ascend_by,
            descend_by,
            condition):
        super().__init__(client=client)

        if len(columns) < 1:
            raise RuntimeError('empty columns')

        if not check_cols(columns, structure.columns):
            raise RuntimeError('invalid columns')

        if ascend_by and not check_cols(ascend_by, columns):
            raise RuntimeError('invalid ascend_by')

        if descend_by and not check_cols(descend_by, columns):
            raise RuntimeError('invalid descend_by')

        if not check_order_by_cols(ascend_by, descend_by):
            raise RuntimeError('invalid ascend_by and descend_by')

        self.__structure = structure
        self.__columns = columns
        self.__ascend_by = ascend_by
        self.__descend_by = descend_by
        self.__condition = condition

    @property
    def structure(self):
        return self.__structure

    @property
    def columns(self):
        return self.__columns

    @property
    def ascend_by(self):
        return self.__ascend_by

    @property
    def descend_by(self):
        return self.__descend_by

    @property
    def condition(self):
        return self.__condition
