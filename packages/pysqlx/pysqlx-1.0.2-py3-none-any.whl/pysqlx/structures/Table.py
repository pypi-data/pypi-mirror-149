

import weakref

from .columntypes import (
    CharStringColumn,
    Column,
    DatetimeColumn,
    FloatColumn,
    IntegerColumn,
    TextColumn,
)
from .Structure import Structure


class Table(Structure):

    def __init__(self, table_name, database=None, schema=None):
        super().__init__(structure_name='table')

        self.__table_name = table_name
        self.__database = database
        self.__schema = schema

        self.__cols = []

    @property
    def table_name(self):
        return self.__table_name

    @property
    def database(self):
        return self.__database

    @property
    def schema(self):
        return self.__schema

    @property
    def columns(self):
        return self.__cols

    def clear_columns(self):
        self.__cols = []
        return self

    def append_column(self, col_obj):
        if not isinstance(col_obj, Column):
            raise RuntimeError('invalid column object')

        if col_obj.table.table_name is not self.table_name:
            raise RuntimeError('column belongs to another table')

        self.__cols.append(col_obj)

        return col_obj

    def append_columns(self, col_objs):
        for obj in col_objs:
            self.append_column(col_obj=obj)
        return self

    def append_char_string_column(
            self,
            column_name,
            is_unicode=False,
            is_fixed=False,
            size=255,
            default_value=None,
            is_primary_key=False,
            is_prevent_null=False):
        return self.append_column(
            col_obj=CharStringColumn(
                column_name=column_name,
                table=weakref.proxy(self),
                is_unicode=is_unicode,
                is_fixed=is_fixed,
                size=size,
                default_value=default_value,
                is_primary_key=is_primary_key,
                is_prevent_null=is_prevent_null
            )
        )

    def append_datetime_column(
            self,
            column_name,
            default_value=None,
            is_primary_key=False,
            is_prevent_null=False):
        return self.append_column(
            col_obj=DatetimeColumn(
                column_name=column_name,
                table=weakref.proxy(self),
                default_value=default_value,
                is_primary_key=is_primary_key,
                is_prevent_null=is_prevent_null
            )
        )

    def append_float_column(
            self,
            column_name,
            is_double=True,
            default_value=None,
            is_primary_key=False,
            is_prevent_null=False):
        return self.append_column(
            col_obj=FloatColumn(
                column_name=column_name,
                table=weakref.proxy(self),
                is_double=is_double,
                default_value=default_value,
                is_primary_key=is_primary_key,
                is_prevent_null=is_prevent_null
            )
        )

    def append_integer_column(
            self,
            column_name,
            n_bytes=4,
            default_value=None,
            is_identity=False,
            is_primary_key=False,
            is_prevent_null=False):
        return self.append_column(
            col_obj=IntegerColumn(
                column_name=column_name,
                table=weakref.proxy(self),
                n_bytes=n_bytes,
                default_value=default_value,
                is_identity=is_identity,
                is_primary_key=is_primary_key,
                is_prevent_null=is_prevent_null
            )
        )

    def append_text_column(
            self,
            column_name,
            is_unicode=False,
            default_value=None,
            is_primary_key=False,
            is_prevent_null=False):
        return self.append_column(
            col_obj=TextColumn(
                column_name=column_name,
                table=weakref.proxy(self),
                is_unicode=is_unicode,
                default_value=default_value,
                is_primary_key=is_primary_key,
                is_prevent_null=is_prevent_null
            )
        )
