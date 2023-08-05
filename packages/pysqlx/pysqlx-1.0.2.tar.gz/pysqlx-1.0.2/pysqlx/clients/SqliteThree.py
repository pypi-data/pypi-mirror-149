

import os
import sqlite3
from datetime import datetime

from ..logger import logger
from ..structures import DatetimeColumn
from .IClient import IClient

_disk_driver = 'disk'
_memory_driver = 'memory'


_support_dict = (
    {
        'sqlite': (
            _disk_driver,
            _memory_driver,
        ),
    },
    (
        _disk_driver,
        _memory_driver,
    )
)


def _convert_fetch_all(ret_list, columns):
    return tuple(
        tuple(
            datetime.fromisoformat(x[i])
            if isinstance(columns[i], DatetimeColumn) else
            x[i]
            for i in range(len(x))
        )
        for x in ret_list
    )


def _get_connection(directory_path, driver_name, database_name, _info):

    if driver_name == _disk_driver:
        file_path = os.path.join(
            directory_path, database_name + '.db')
    elif driver_name == _memory_driver:
        file_path = ':memory:'

    _info('opening database at "%s"' % file_path)

    try:
        if driver_name == _disk_driver:
            conn = sqlite3.connect(
                'file:%s' % file_path,
                isolation_level=None,
                uri=True
            )
        else:
            conn = sqlite3.connect(
                file_path,
                isolation_level=None
            )
    except Exception as e:
        raise RuntimeError(
            'could not open database, check file permissions') from e

    return conn


class SqliteThree(IClient):

    @staticmethod
    def get_client_name():
        return 'SqliteThree'

    @staticmethod
    def get_dialects_names():
        return tuple(x for x in _support_dict[0])

    @staticmethod
    def get_preferred_drivers(dialect_name):
        return _support_dict[0][dialect_name]

    @staticmethod
    def get_system_drivers():
        return _support_dict[1]

    def __init__(
            self,
            directory_path,
            dialect_name,
            driver_name,
            database_name):
        super().__init__(
            database_name=database_name,
        )

        if driver_name is None:
            driver_name = self._get_default_driver(dialect_name)

        if not self._is_valid_driver(dialect_name, driver_name):
            raise RuntimeError(
                'driver_name is invalid "%s"' % str(driver_name))

        if driver_name == _disk_driver:
            directory_path = os.path.abspath(directory_path)

            if not self._is_valid_directory_path(directory_path):
                raise RuntimeError(
                    'directory_path is invalid "%s"' % str(directory_path))

        self._set_connection(_get_connection(
            directory_path,
            driver_name,
            database_name,
            logger.info,
        ))
        self._set_dialect(dialect_name)

    def _execute_sql_string(self, sql_string, param_tuple):

        cur = self._connection.cursor()

        if param_tuple:
            cur.execute(sql_string, param_tuple)
        else:
            cur.execute(sql_string)

        return cur

    def _execute_many_sql_string(self, sql_string, param_tuple_list):
        return self._connection.cursor().executemany(
            sql_string, param_tuple_list)

    def _execute_Create(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_Delete(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_Drop(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_GetLength(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        return ret[0][0]

    def _execute_Insert(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_IsEmpty(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        return True if (ret and ret[0][0] == 0) else False

    def _execute_IsExists(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        table = query.structure
        return True if (ret and ret[0][0] == table.table_name) else False

    def _execute_Select(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        return _convert_fetch_all(ret, query.columns)

    def _execute_SelectDistinct(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        return _convert_fetch_all(ret, query.columns)

    def _execute_Truncate(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_Union(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug('received "%s"' % str(ret))

        return _convert_fetch_all(ret, query.columns_list[0])

    def _execute_Update(self, query, param_tuple):
        self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        )

    def _execute_many_Insert(self, query, param_tuple_list):
        self._execute_many(
            sql_string=self.get_query_string(query),
            param_tuple_list=param_tuple_list
        )

    def _execute_many_Update(self, query, param_tuple_list):
        self._execute_many(
            sql_string=self.get_query_string(query),
            param_tuple_list=param_tuple_list
        )

    def backup_to(self, other):
        from_db = self._connection
        to_db = other._connection
        with from_db, to_db:
            from_db.backup(to_db)
