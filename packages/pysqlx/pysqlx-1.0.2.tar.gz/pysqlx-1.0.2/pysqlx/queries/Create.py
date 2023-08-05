

from .Query import Query


class Create(Query):

    def __init__(self, client, structure):
        super().__init__(client=client)

        self.__structure = structure

    @property
    def structure(self):
        return self.__structure
