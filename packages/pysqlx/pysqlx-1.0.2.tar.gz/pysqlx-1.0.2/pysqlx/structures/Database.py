

from .Structure import Structure


class Database(Structure):

    def __init__(self, database_name):
        super().__init__(structure_name='database')

        self.__database_name = database_name

    @property
    def database_name(self):
        return self.__database_name
