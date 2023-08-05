

from datetime import datetime

from ..structures import Clause, Column
from .IDialect import IDialect

_int_name_dict = {
    1: 'tinyint',
    2: 'smallint',
    4: 'int',
    8: 'bigint',
}


class MsSql(IDialect):

    def __init__(self):
        super().__init__(dialect_name='mssql')

    def get_table_qualifier(self, table):
        q_ar = []

        if table.database and table.schema:
            q_ar.append(table.database.database_name)

        if table.schema:
            q_ar.append(table.schema.schema_name)

        q_ar.append(table.table_name)

        return '.'.join('[' + x + ']' for x in q_ar)

    def get_column_qualifier(self, column):
        return '[' + column.column_name + ']'

    def _get_common_declaration_string(self, column, type_string):
        return ' '.join(tuple(
            x
            for x in (
                column.column_name,
                type_string,
                'NOT NULL' if column.is_prevent_null else '',
                'IDENTITY(1, 1)' if column.is_identity else '',
                'DEFAULT %s' % str(column.default_value)
                if column.default_value else '',
            ) if x != ''
        ))

    def get_CharStringColumn_declaration(self, column):
        type_string = ''

        if column.is_unicode:
            type_string += 'n'

        if not column.is_fixed:
            type_string += 'var'

        type_string += 'char(%s)' % str(column.size)

        return self._get_common_declaration_string(column, type_string)

    def get_DatetimeColumn_declaration(self, column):
        return self._get_common_declaration_string(
            column, type_string='datetime')

    def get_FloatColumn_declaration(self, column):
        return self._get_common_declaration_string(
            column,
            type_string='float(%s)' %
            (str(53) if column.is_double else str(24))
        )

    def get_IntegerColumn_declaration(self, column):
        return self._get_common_declaration_string(
            column, type_string=_int_name_dict[column.n_bytes])

    def get_TextColumn_declaration(self, column):
        type_string = ''

        if column.is_unicode:
            type_string += 'n'

        type_string += 'varchar(max)'

        return self._get_common_declaration_string(column, type_string)

    def _convert_value(self, val):
        if isinstance(val, str):
            return '\'' + val + '\''

        if isinstance(val, datetime):
            return self._convert_value(
                val.isoformat(timespec='milliseconds'))

        if isinstance(val, (int, float)):
            return str(val)

        if isinstance(val, Clause):
            return ''.join([
                '(',
                self.get_clause_string(val),
                ')',
            ])

        if isinstance(val, Column):
            return self.get_column_qualifier(val)

        raise RuntimeError(
            'unknown value "%s" of type "%s"' % (str(val), type(val).__name__))

    def get_And_string(self, clause):
        return ' '.join((
            self._convert_value(clause.clause0),
            'AND',
            self._convert_value(clause.clause1),
        ))

    def get_Between_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'BETWEEN',
            self._convert_value(clause.value0),
            'AND',
            self._convert_value(clause.value1),
        ))

    def get_Equal_string(self, clause):
        return ' = '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_GreaterThan_string(self, clause):
        return ' > '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_GreaterThanEqual_string(self, clause):
        return ' >= '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_InList_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'IN (',
            ', '.join(tuple(
                self._convert_value(val)
                for val in clause.val_list)),
            ')',
        ))

    def get_IsNotNull_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'IS NOT NULL',
        ))

    def get_IsNull_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'IS NULL',
        ))

    def get_LessThan_string(self, clause):
        return ' < '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_LessThanEqual_string(self, clause):
        return ' <= '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_Like_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'LIKE',
            self._convert_value(clause.value),
        ))

    def get_NotBetween_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'NOT BETWEEN',
            self._convert_value(clause.value0),
            'AND',
            self._convert_value(clause.value1),
        ))

    def get_NotEqual_string(self, clause):
        return ' != '.join((
            self._convert_value(clause.lhs),
            self._convert_value(clause.rhs),
        ))

    def get_NotInList_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'NOT IN (',
            ', '.join(tuple(
                self._convert_value(val)
                for val in clause.val_list)),
            ')',
        ))

    def get_NotLike_string(self, clause):
        return ' '.join((
            self._convert_value(clause.column),
            'NOT LIKE',
            self._convert_value(clause.value),
        ))

    def get_Or_string(self, clause):
        return ' '.join((
            self._convert_value(clause.clause0),
            'OR',
            self._convert_value(clause.clause1),
        ))

    def get_Create_database_string(self, query):
        database = query.structure

        return 'CREATE DATABASE %s' % database.database_name

    def get_Create_schema_string(self, query):
        schema = query.structure

        sql_string = 'CREATE SCHEMA %s' % schema.schema_name

        if not schema.owner_name:
            return sql_string

        return '%s AUTHORIZATION %s' % (sql_string, schema.owner_name)

    def get_Create_table_string(self, query):
        table = query.structure

        if not table.columns:
            raise RuntimeError('table has no columns')

        table_cols = [
            self.get_column_declaration(col)
            for col in table.columns
        ]
        table_keys = tuple(
            col.column_name
            for col in table.columns if col.is_primary_key
        )

        if table_keys:
            table_cols.append('PRIMARY KEY (%s)' % ', '.join(table_keys))

        return 'CREATE TABLE %s (\n%s\n)' % (
            self.get_table_qualifier(table),
            ',\n'.join(table_cols),
        )

    def get_Delete_table_string(self, query):
        table = query.structure
        condition = query.condition

        return ' '.join((
            'DELETE FROM',
            self.get_table_qualifier(table),
            'WHERE',
            self.get_clause_string(condition),
        ))

    def get_Drop_database_string(self, query):
        database = query.structure

        return 'DROP DATABASE %s' % database.database_name

    def get_Drop_schema_string(self, query):
        schema = query.structure

        return 'DROP SCHEMA %s' % schema.schema_name

    def get_Drop_table_string(self, query):
        table = query.structure

        return 'DROP TABLE %s' % self.get_table_qualifier(table)

    def get_GetLength_table_string(self, query):
        table = query.structure

        return 'SELECT COUNT(*) FROM %s' % self.get_table_qualifier(table)

    def get_Insert_table_string(self, query):
        table = query.structure
        columns = query.columns

        col_names = tuple(
            self.get_column_qualifier(col)
            for col in columns
        )

        return 'INSERT INTO %s (%s) VALUES (%s)' % (
            self.get_table_qualifier(table),
            ',\n'.join(col_names),
            ', '.join(['?'] * len(col_names))
        )

    def get_IsEmpty_table_string(self, query):
        table = query.structure

        return 'SELECT COUNT(*) FROM %s' % self.get_table_qualifier(table)

    def get_IsExists_database_string(self, query):
        database = query.structure

        return '''if exists (
    SELECT name FROM master.sys.databases WHERE name='%s')
    SELECT 1 AS result;
else
    SELECT 0 AS result;''' % database.database_name

    def get_IsExists_schema_string(self, query):
        schema = query.structure

        return '''if exists (
    SELECT schema_name FROM information_schema.schemata WHERE schema_name='%s')
    SELECT 1 AS result;
else
    SELECT 0 AS result;''' % schema.schema_name

    def get_IsExists_table_string(self, query):
        table = query.structure

        return '''if exists (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'
    AND TABLE_NAME='%s')
    SELECT 1 AS result;
else
    SELECT 0 AS result;''' % table.table_name

    def get_Select_table_string(self, query):
        table = query.structure
        top = query.top
        columns = query.columns
        ascend_by = query.ascend_by
        descend_by = query.descend_by
        condition = query.condition

        sql_ar = [
            'SELECT',
            '' if top is None else 'TOP (%s)' % str(top),
            ',\n'.join(tuple(
                self.get_column_qualifier(col)
                for col in columns
            )),
            'FROM',
            self.get_table_qualifier(table),
        ]

        if condition:
            sql_ar += [
                'WHERE',
                self.get_clause_string(condition),
            ]

        if any((ascend_by, descend_by)):
            order_ar = []

            if ascend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' ASC'
                    for col in ascend_by
                ]

            if descend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' DESC'
                    for col in descend_by
                ]

            sql_ar += [
                'ORDER BY',
                ',\n'.join(order_ar),
            ]

        return ' '.join(tuple(
            x
            for x in sql_ar if x != ''
        ))

    def get_SelectDistinct_table_string(self, query):
        table = query.structure
        columns = query.columns
        ascend_by = query.ascend_by
        descend_by = query.descend_by
        condition = query.condition

        sql_ar = [
            'SELECT DISTINCT',
            ', '.join(tuple(
                self.get_column_qualifier(col)
                for col in columns
            )),
            'FROM',
            self.get_table_qualifier(table),
        ]

        if condition:
            sql_ar += [
                'WHERE',
                self.get_clause_string(condition),
            ]

        if any((ascend_by, descend_by)):
            order_ar = []

            if ascend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' ASC'
                    for col in ascend_by
                ]

            if descend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' DESC'
                    for col in descend_by
                ]

            sql_ar += [
                'ORDER BY',
                ', '.join(order_ar),
            ]

        return ' '.join(sql_ar)

    def get_Truncate_table_string(self, query):
        table = query.structure

        return 'TRUNCATE TABLE %s' % self.get_table_qualifier(table)

    def get_Union_table_string(self, query):
        table_list = query.structure_list
        query_list = query.query_list
        columns_list = query.columns_list
        is_all = query.is_all
        ascend_by = query.ascend_by
        descend_by = query.descend_by
        condition = query.condition

        union_str = ('\nUNION%s\n' % (' ALL' if is_all else '')).join(
            tuple(
                ' '.join([
                    'SELECT',
                    ',\n'.join(tuple(
                        self.get_column_qualifier(col)
                        for col in columns_list[i]
                    )),
                    'FROM',
                    '(\n' + self.get_query_string(query_list[i]) + '\n)',
                    table_list[i].table_name
                ])
                for i in range(len(table_list))
            )
        ) + '\n'

        if condition:
            union_str += 'WHERE\n' + \
                self.get_clause_string(condition)

        if any((ascend_by, descend_by)):
            order_ar = []

            if ascend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' ASC'
                    for col in ascend_by
                ]

            if descend_by:
                order_ar += [
                    self.get_column_qualifier(col) + ' DESC'
                    for col in descend_by
                ]

            union_str += 'ORDER BY\n' + ',\n'.join(order_ar)

        return union_str

    def get_Update_table_string(self, query):
        table = query.structure
        columns = query.columns
        condition = query.condition

        col_names = tuple(
            self.get_column_qualifier(col)
            for col in columns
        )

        return 'UPDATE %s\nSET %s\nWHERE %s' % (
            self.get_table_qualifier(table),
            ', '.join(tuple(
                col + '=?'
                for col in col_names
            )),
            self.get_clause_string(condition),
        )
