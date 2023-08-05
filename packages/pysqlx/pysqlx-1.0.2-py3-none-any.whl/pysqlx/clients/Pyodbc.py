

from time import time

import pyodbc

from ..logger import logger
from .IClient import IClient

_support_dict = (
    {
        'mssql': (
            'ODBC Driver 17 for SQL Server',
            'ODBC Driver 13.1 for SQL Server',
            'ODBC Driver 13 for SQL Server',
            'ODBC Driver 11 for SQL Server',
            'SQL Server Native Client 11.0',
            'SQL Server Native Client 10.0',
            'SQL Native Client',
            'SQL Server',
            'PSQL',
        ),
    },
    pyodbc.drivers(),
)


def _convert_fetch_all(ret_list, _columns):
    return tuple(
        tuple(
            x[i]
            for i in range(len(x))
        )
        for x in ret_list
    )


def _get_connection(
        server_address,
        user_name,
        user_pass,
        server_port,
        is_trusted_connection,
        driver_name,
        database_name,
        _info):

    tic = time()

    _info(f'authenticating for user "{user_name}"')

    conn_ar = [
        f'DRIVER={driver_name}',
        f'UID={user_name}',
    ]

    if server_port:
        conn_ar.append(
            f'SERVER={server_address},{str(server_port)}'
        )
    else:
        conn_ar.append(f'SERVER={server_address}')

    if database_name:
        conn_ar.append(f'DATABASE={database_name}')

    if is_trusted_connection:
        conn_ar.append('Trusted_Connection=Yes')

    conn_ar.append('PWD=')

    _info(f"connection string \"{';'.join(conn_ar)}*\"")

    try:
        conn = pyodbc.connect(
            ';'.join(conn_ar) + user_pass,
            autocommit=True
        )
    except Exception as e:
        raise RuntimeError(
            'could not authenticate DB, check username and password') from e

    _info(f'connection initalized in {str(time() - tic)} seconds')

    return conn


class Pyodbc(IClient):

    @staticmethod
    def get_client_name():
        return 'Pyodbc'

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
            server_address,
            user_name,
            user_pass,
            server_port,
            is_trusted_connection,
            dialect_name,
            driver_name,
            database_name):
        super().__init__(
            database_name=database_name,
        )

        if not self._is_valid_server_address(server_address):
            raise RuntimeError(
                f'server_address is invalid "{str(server_address)}"')

        if not self._is_valid_user_name(user_name):
            raise RuntimeError(f'username is invalid "{str(user_name)}"')

        if not self._is_valid_user_pass(user_pass):
            raise RuntimeError('password is invalid')

        if not self._is_valid_server_port(server_port):
            raise RuntimeError(
                f'server_port is invalid "{str(server_port)}"')

        if not isinstance(is_trusted_connection, bool):
            raise RuntimeError(
                'is_trusted_connection is invalid '
                f'"{str(is_trusted_connection)}"')

        if driver_name is None:
            driver_name = self._get_default_driver(dialect_name)

        if not self._is_valid_driver(dialect_name, driver_name):
            raise RuntimeError(
                f'driver_name is invalid "{str(driver_name)}"')

        self._set_connection(
            _get_connection(
                server_address,
                user_name,
                user_pass,
                server_port,
                is_trusted_connection,
                driver_name,
                database_name,
                logger.info
            )
        )
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

        logger.debug(f'received "{ret}"')

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

        logger.debug(f'received "{ret}"')

        return True if (ret and ret[0][0] == 0) else False

    def _execute_IsExists(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug(f'received "{ret}"')

        return ret[0][0] == 1

    def _execute_Select(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug(f'received "{ret}"')

        return _convert_fetch_all(ret, query.columns)

    def _execute_SelectDistinct(self, query, param_tuple):
        ret = self._execute(
            sql_string=self.get_query_string(query),
            param_tuple=param_tuple
        ).fetchall()

        logger.debug(f'received "{ret}"')

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

        logger.debug(f'received "{ret}"')

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
