

from .Query import Query
from .Select import Select
from .utility import check_cols, check_order_by_cols


class Union(Query):

    def __init__(
            self,
            client,
            structure_list,
            query_list,
            columns_list,
            is_all,
            ascend_by,
            descend_by,
            condition):
        super().__init__(client=client)

        if not structure_list:
            raise RuntimeError('empty structure_list')

        if not query_list:
            raise RuntimeError('empty query_list')

        if len(query_list) != len(structure_list):
            raise RuntimeError('query_list and structure_list size mismatch')

        for query in query_list:
            if not isinstance(query, Select):
                raise RuntimeError(
                    'invalid query of type "%s"' % type(query).__name__)

        if not columns_list:
            columns_list = [None] * len(structure_list)

        if len(columns_list) != len(structure_list):
            raise RuntimeError(
                'columns_list and structure_list size mismatch')

        for i in range(len(columns_list)):
            if not columns_list[i]:
                columns_list[i] = structure_list[i].columns

            if not check_cols(columns_list[i], structure_list[i].columns):
                raise RuntimeError('invalid columns')

            if ascend_by and not check_cols(ascend_by, columns_list[i]):
                raise RuntimeError('invalid ascend_by')

            if descend_by and not check_cols(descend_by, columns_list[i]):
                raise RuntimeError('invalid descend_by')

        if not check_order_by_cols(ascend_by, descend_by):
            raise RuntimeError('invalid ascend_by and descend_by')

        if not isinstance(is_all, bool):
            raise RuntimeError('invalid is_all "%s"' % str(is_all))

        self.__structure_list = structure_list
        self.__query_list = query_list
        self.__columns_list = columns_list
        self.__is_all = is_all
        self.__ascend_by = ascend_by
        self.__descend_by = descend_by
        self.__condition = condition

    @property
    def structure_list(self):
        return self.__structure_list

    @property
    def query_list(self):
        return self.__query_list

    @property
    def columns_list(self):
        return self.__columns_list

    @property
    def is_all(self):
        return self.__is_all

    @property
    def ascend_by(self):
        return self.__ascend_by

    @property
    def descend_by(self):
        return self.__descend_by

    @property
    def condition(self):
        return self.__condition
