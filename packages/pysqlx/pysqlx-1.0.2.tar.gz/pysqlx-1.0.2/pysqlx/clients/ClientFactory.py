

from .Pyodbc import Pyodbc
from .SqliteThree import SqliteThree

_support_dict = {
    'sqlite3': SqliteThree,
    'pyodbc': Pyodbc,
}


class ClientFactory:

    @staticmethod
    def get_providers_names():
        return tuple(x for x in _support_dict)

    @staticmethod
    def get_dialects_names(provider_name):
        return _support_dict[provider_name].get_dialects_names()

    @staticmethod
    def get_preferred_drivers(provider_name, dialect_name):
        return _support_dict[provider_name].get_preferred_drivers(
            dialect_name=dialect_name)

    @staticmethod
    def get_system_drivers(provider_name):
        return _support_dict[provider_name].get_system_drivers()

    @staticmethod
    def get_sqlite3_client(
            directory_path,
            dialect_name,
            driver_name,
            database_name):
        return SqliteThree(
            directory_path=directory_path,
            dialect_name=dialect_name,
            driver_name=driver_name,
            database_name=database_name,
        )

    @staticmethod
    def get_pyodbc_client(
            server_address,
            user_name,
            user_pass,
            dialect_name,
            server_port=None,
            is_trusted_connection=False,
            driver_name=None,
            database_name=None):
        return Pyodbc(
            server_address=server_address,
            user_name=user_name,
            user_pass=user_pass,
            server_port=server_port,
            is_trusted_connection=is_trusted_connection,
            dialect_name=dialect_name,
            driver_name=driver_name,
            database_name=database_name,
        )
