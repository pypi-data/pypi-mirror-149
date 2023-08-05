

from .Column import Column


class TextColumn(Column):

    def __init__(
            self,
            column_name,
            table,
            is_unicode,
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

        self.__is_unicode = is_unicode

    @property
    def is_unicode(self):
        return self.__is_unicode
