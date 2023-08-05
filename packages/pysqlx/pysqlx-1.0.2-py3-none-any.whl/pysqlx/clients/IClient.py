

import os
from abc import ABC, abstractmethod
from time import time

from ..dialects import MsSql, Sqlite
from ..logger import logger
from ..queries import (  # GetTableObject,
    Create,
    Delete,
    Drop,
    GetLength,
    Insert,
    IsEmpty,
    IsExists,
    Select,
    SelectDistinct,
    Truncate,
    Union,
    Update,
)


class IClient(ABC):

    @staticmethod
    @abstractmethod
    def get_client_name():
        pass

    @staticmethod
    @abstractmethod
    def get_dialects_names():
        pass

    @staticmethod
    @abstractmethod
    def get_preferred_drivers(dialect_name):
        pass

    @staticmethod
    @abstractmethod
    def get_system_drivers():
        pass

    def __init__(self, database_name):
        ABC.__init__(self)

        if not self._is_valid_database_name(database_name):
            raise RuntimeError(
                f'database_name is invalid "{str(database_name)}"')

        self.__database_name = database_name
        self.__dialect = None
        self.__conn = None

    def __del__(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

        logger.debug('connection closed')

    @property
    def database_name(self):
        return self.__database_name

    @property
    def dialect_name(self):
        return self.__dialect.dialect_name

    @property
    def _connection(self):
        return self.__conn

    def _is_valid_directory_path(self, directory_path):
        return isinstance(
            directory_path,
            str) and os.path.exists(directory_path)

    def _is_valid_server_address(self, server_address):
        return isinstance(server_address, str) and server_address != ''

    def _is_valid_user_name(self, user_name):
        return isinstance(user_name, str) and user_name != ''

    def _is_valid_user_pass(self, user_pass):
        return isinstance(user_pass, str) and user_pass != ''

    def _is_valid_server_port(self, server_port):
        return any((
            server_port is None,
            isinstance(server_port, int),
        ))

    def _is_valid_database_name(self, database_name):
        return any((
            database_name is None,
            isinstance(database_name, str) and database_name != '',
        ))

    def _is_valid_driver(self, dialect_name, driver_name):
        return all((
            driver_name in self.get_system_drivers(),
            driver_name in self.get_preferred_drivers(
                dialect_name=dialect_name),
        ))

    def _get_default_driver(self, dialect_name):
        sys_drivers = self.get_system_drivers()
        for driver_name in self.get_preferred_drivers(
                dialect_name=dialect_name):
            if driver_name in sys_drivers:
                return driver_name
        raise RuntimeError('Could not find a valid driver')

    def _set_dialect(self, dialect_name):

        if dialect_name not in self.get_dialects_names():
            raise RuntimeError(
                f'dialect_name is invalid "{str(dialect_name)}"')

        if dialect_name == 'sqlite':
            obj = Sqlite()
        elif dialect_name == 'mssql':
            obj = MsSql()
        else:
            raise RuntimeError(f'unsupported dialect "{dialect_name}"')

        self.__dialect = obj

    def _set_connection(self, obj):
        self.__conn = obj

    def get_query_string(self, query):
        return self.__dialect.get_query_string(query)

    def _execute(self, sql_string, param_tuple=None):
        tic = time()

        if not sql_string:
            raise RuntimeError('invalid SQL request')

        if param_tuple:
            logger.debug(
                f'executing "{sql_string}" with parameters '
                f'"{str(param_tuple)}"')
        else:
            logger.debug(f'executing "{sql_string}"')

        cur = self._execute_sql_string(
            sql_string=sql_string,
            param_tuple=param_tuple,
        )

        logger.debug(f'executed in {str(time() - tic)} seconds')

        return cur

    def _execute_many(self, sql_string, param_tuple_list):
        tic = time()

        if not sql_string:
            raise RuntimeError('invalid SQL request')

        logger.debug(
            f'executing "{sql_string}" with many parameters '
            f'"{str(param_tuple_list)}"')

        cur = self._execute_many_sql_string(
            sql_string=sql_string,
            param_tuple_list=param_tuple_list,
        )

        logger.debug(f'executed in {str(time() - tic)} seconds')

        return cur

    def execute(self, query, param_tuple=None):
        return getattr(
            self,
            '_execute_' + type(query).__name__,
        )(
            query=query,
            param_tuple=param_tuple,
        )

    def execute_many(self, query, param_tuple_list):
        return getattr(
            self,
            '_execute_many_' + type(query).__name__,
        )(
            query=query,
            param_tuple_list=param_tuple_list,
        )

    @abstractmethod
    def _execute_sql_string(self, sql_string, param_tuple):
        pass

    @abstractmethod
    def _execute_many_sql_string(self, sql_string, param_tuple_list):
        pass

    @abstractmethod
    def _execute_Create(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Delete(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Drop(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_GetLength(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Insert(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_IsEmpty(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_IsExists(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Select(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_SelectDistinct(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Truncate(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Union(self, query, param_tuple):
        pass

    @abstractmethod
    def _execute_Update(self, query, param_tuple):
        pass

    def _execute_many_Create(self, query, param_tuple_list):
        raise RuntimeError('Create query does not support execute_many')

    def _execute_many_Delete(self, query, param_tuple_list):
        raise RuntimeError('Delete query does not support execute_many')

    def _execute_many_Drop(self, query, param_tuple_list):
        raise RuntimeError('Drop query does not support execute_many')

    def _execute_many_GetLength(self, query, param_tuple_list):
        raise RuntimeError('GetLength query does not support execute_many')

    @abstractmethod
    def _execute_many_Insert(self, query, param_tuple_list):
        pass

    def _execute_many_IsEmpty(self, query, param_tuple_list):
        raise RuntimeError('IsEmpty query does not support execute_many')

    def _execute_many_IsExists(self, query, param_tuple_list):
        raise RuntimeError('IsExists query does not support execute_many')

    def _execute_many_Select(self, query, param_tuple_list):
        raise RuntimeError('Select query does not support execute_many')

    def _execute_many_SelectDistinct(self, query, param_tuple_list):
        raise RuntimeError(
            'SelectDistinct query does not support execute_many')

    def _execute_many_Truncate(self, query, param_tuple_list):
        raise RuntimeError('Truncate query does not support execute_many')

    def _execute_many_Union(self, query, param_tuple_list):
        raise RuntimeError('Union query does not support execute_many')

    @abstractmethod
    def _execute_many_Update(self, query, param_tuple_list):
        pass

    def create(self, structure):
        return Create(client=self, structure=structure)

    def delete(self, structure, condition):
        return Delete(client=self, structure=structure, condition=condition)

    def drop(self, structure):
        return Drop(client=self, structure=structure)

    def is_exists(self, structure):
        return IsExists(client=self, structure=structure)

    def is_empty(self, structure):
        return IsEmpty(client=self, structure=structure)

    def get_length(self, structure):
        return GetLength(client=self, structure=structure)

    # def get_table_object(self, table_name, schema_name=None):
    #     return GetTableObject(
    #         client=self,
    #         table_name=table_name,
    #         schema_name=schema_name
    #     )

    def truncate(self, structure):
        return Truncate(client=self, structure=structure)

    def insert(self, structure, columns=None):
        return Insert(client=self, structure=structure, columns=columns)

    def select(
            self,
            structure,
            columns=None,
            top=None,
            ascend_by=None,
            descend_by=None,
            condition=None):
        return Select(
            client=self,
            structure=structure,
            columns=columns,
            top=top,
            ascend_by=ascend_by,
            descend_by=descend_by,
            condition=condition,
        )

    def select_distinct(
            self,
            structure,
            columns,
            ascend_by=None,
            descend_by=None,
            condition=None):
        return SelectDistinct(
            client=self,
            structure=structure,
            columns=columns,
            ascend_by=ascend_by,
            descend_by=descend_by,
            condition=condition,
        )

    def union(
            self,
            structure_list,
            query_list,
            columns_list=None,
            is_all=False,
            ascend_by=None,
            descend_by=None,
            condition=None):
        return Union(
            client=self,
            structure_list=structure_list,
            query_list=query_list,
            columns_list=columns_list,
            is_all=is_all,
            ascend_by=ascend_by,
            descend_by=descend_by,
            condition=condition,
        )

    def update(
            self,
            structure,
            condition,
            columns=None):
        return Update(
            client=self,
            structure=structure,
            columns=columns,
            condition=condition,
        )
