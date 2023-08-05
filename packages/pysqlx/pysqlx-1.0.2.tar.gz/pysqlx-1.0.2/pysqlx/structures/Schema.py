

from .Structure import Structure


class Schema(Structure):

    def __init__(self, schema_name, owner_name=None):
        super().__init__(structure_name='schema')

        self.__schema_name = schema_name
        self.__owner_name = owner_name

    @property
    def schema_name(self):
        return self.__schema_name

    @property
    def owner_name(self):
        return self.__owner_name
