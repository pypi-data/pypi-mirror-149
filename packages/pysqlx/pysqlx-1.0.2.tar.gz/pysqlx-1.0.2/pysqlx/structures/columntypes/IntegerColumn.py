

from .Column import Column

_valid_bytes = (
    1,
    2,
    4,
    8,
)


class IntegerColumn(Column):

    def __init__(
            self,
            column_name,
            table,
            n_bytes,
            default_value,
            is_identity,
            is_primary_key,
            is_prevent_null):
        super().__init__(
            column_name=column_name,
            table=table,
            default_value=default_value,
            is_identity=is_identity,
            is_primary_key=is_primary_key,
            is_prevent_null=is_prevent_null
        )

        assert(isinstance(n_bytes, int))
        assert(n_bytes in _valid_bytes)

        self.__n_bytes = n_bytes

    @property
    def n_bytes(self):
        return self.__n_bytes
