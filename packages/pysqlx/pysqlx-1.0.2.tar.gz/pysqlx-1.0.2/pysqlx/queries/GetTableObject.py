

from .Query import Query

_support_dict = {
    'sqlite': (
        'table',
    ),
    'mssql': (
        'table',
    )
}

_sqlite_int_types = {
    'tinyint': 1,
    'smallint': 2,
    'int2': 2,
    'int': 4,
    'integer': 4,
    'mediumint': 4,
    'bigint': 8,
    'unsigned big int': 8,
    'int8': 8,
}

_sqlite_id_idx = 0         # cid
_sqlite_col_name_idx = 1   # name
_sqlite_data_type_idx = 2  # type
_sqlite_is_null_idx = 3    # notnull
_sqlite_default_idx = 4    # dflt_value
_sqlite_is_pk_idx = 5      # pk

_mssql_col_name_col = 'COLUMN_NAME'
_mssql_is_null_col = 'IS_NULLABLE'
_mssql_data_type_col = 'DATA_TYPE'
_mssql_max_len_col = 'CHARACTER_MAXIMUM_LENGTH'
_mssql_num_prec_col = 'NUMERIC_PRECESSION'


def _append_sqlite(table, row):
    column_name = row[_sqlite_col_name_idx]
    type_str = row[_sqlite_data_type_idx].lower()
    is_prevent_null = row[_sqlite_is_null_idx] != 0
    default_value = row[_sqlite_default_idx]
    is_primary_key = row[_sqlite_is_pk_idx] != 0

    if type_str == 'datetime':
        table.append_datetime_column(
            column_name=column_name,
            default_value=default_value,
            is_primary_key=is_primary_key,
            is_prevent_null=is_prevent_null
        )
    elif type_str in _sqlite_int_types:
        table.append_integer_column(
            column_name=column_name,
            n_bytes=_sqlite_int_types[type_str],
            default_value=default_value,
            is_identity=False,
            is_primary_key=is_primary_key,
            is_prevent_null=is_prevent_null
        )
    else:
        raise RuntimeError('unknown column type "%s"' % type_str)


def _append_mssql(table, row):
    print(row)


class GetTableObject(Query):

    def __init__(self, client, table_name, schema_name):
        super().__init__(client=client)

        if client.dialect_name not in _support_dict:
            raise RuntimeError(
                'unsupported dialect "%s"' % client.dialect_name)

        from ..structures import Database, Schema, Table

        database = Database(database_name=client.database_name) \
            if client.database_name else None
        schema = Schema(schema_name=schema_name) if schema_name else None

        self.__table = Table(
            table_name=table_name,
            database=database,
            schema=schema
        )

    def _sqlite_table(self):
        table = self.__table

        # return 'SELECT * FROM PRAGMA_TABLE_INFO(\'%s\')' % \
        #     table.get_table_qualifier(dialect_name='sqlite')

        return 'SELECT sql FROM sqlite_master WHERE name=\'%s\'' % \
            table.get_table_qualifier(dialect_name='sqlite')

    def _mssql_table(self):
        table = self.__table

        return 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s' % \
            table.get_table_qualifier(dialect_name='mssql')

    def _sqlite3_execute_ret(self):

        for row in super()._execute().fetchall():
            print(row)
            #_append_sqlite(self.__table, row)

        return self.__table

    def _pyobdc_execute_ret(self):

        for row in super()._execute().fetchall():
            _append_mssql(self.__table, row)

        return self.__table

    def get_sql_string(self):
        return getattr(self, '_' + self.client.dialect_name + '_table')()

    def execute(self):
        return getattr(
            self,
            '_' + self.client.provider_name +
            '_execute_ret'
        )()
