

from .Column import Column


class FloatColumn(Column):

    def __init__(
            self,
            column_name,
            table,
            is_double,
            default_value,
            is_primary_key,
            is_prevent_null):
        super().__init__(
            column_name=column_name,
            table=table,
            default_value=default_value,
            is_identity=False,
            is_primary_key=is_primary_key,
            is_prevent_null=is_prevent_null
        )

        assert(isinstance(is_double, bool))

        self.__is_double = is_double

    @property
    def is_double(self):
        return self.__is_double
