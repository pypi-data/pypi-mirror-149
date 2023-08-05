

from .Query import Query


class Delete(Query):

    def __init__(self, client, structure, condition):
        super().__init__(client=client)

        self.__structure = structure
        self.__condition = condition

    @property
    def structure(self):
        return self.__structure

    @property
    def condition(self):
        return self.__condition
