

from ..Structure import Structure
from .logicalclause import (
    Between,
    Equal,
    GreaterThan,
    GreaterThanEqual,
    InList,
    IsNotNull,
    IsNull,
    LessThan,
    LessThanEqual,
    Like,
    NotEqual,
)


class Column(Structure):

    def __init__(
            self,
            column_name,
            table,
            default_value,
            is_identity,
            is_primary_key,
            is_prevent_null):
        super().__init__(structure_name='column')

        if is_identity or is_primary_key:
            is_prevent_null = True

        if default_value and any((is_identity, is_primary_key)):
            raise RuntimeError('invalid default value settings')

        self.__column_name = column_name
        self.__table = table
        self.__default_value = default_value
        self.__is_identity = is_identity
        self.__is_primary_key = is_primary_key
        self.__is_prevent_null = is_prevent_null

    @property
    def column_name(self):
        return self.__column_name

    @property
    def table(self):
        return self.__table

    @property
    def default_value(self):
        return self.__default_value

    @property
    def is_identity(self):
        return self.__is_identity

    @property
    def is_primary_key(self):
        return self.__is_primary_key

    @property
    def is_prevent_null(self):
        return self.__is_prevent_null

    def get_index(self):
        return self.table.columns.index(self)

    def __eq__(self, other):
        return Equal(lhs=self, rhs=other)

    def __ne__(self, other):
        return NotEqual(lhs=self, rhs=other)

    def __gt__(self, other):
        return GreaterThan(lhs=self, rhs=other)

    def __ge__(self, other):
        return GreaterThanEqual(lhs=self, rhs=other)

    def __lt__(self, other):
        return LessThan(lhs=self, rhs=other)

    def __le__(self, other):
        return LessThanEqual(lhs=self, rhs=other)

    def is_between(self, value0, value1):
        return Between(column=self, value0=value0, value1=value1)

    def is_in_list(self, val_list):
        return InList(column=self, val_list=val_list)

    def is_null(self):
        return IsNull(column=self)

    def is_not_null(self):
        return IsNotNull(column=self)

    def is_like(self, other):
        return Like(column=self, value=other)
