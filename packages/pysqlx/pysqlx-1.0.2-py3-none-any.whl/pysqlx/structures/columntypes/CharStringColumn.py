

from .Column import Column


class CharStringColumn(Column):

    def __init__(
            self,
            column_name,
            table,
            is_unicode,
            is_fixed,
            size,
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

        assert(isinstance(is_unicode, bool))
        assert(isinstance(is_fixed, bool))
        assert(isinstance(size, int))

        self.__is_unicode = is_unicode
        self.__is_fixed = is_fixed
        self.__size = size

    @property
    def is_unicode(self):
        return self.__is_unicode

    @property
    def is_fixed(self):
        return self.__is_fixed

    @property
    def size(self):
        return self.__size
