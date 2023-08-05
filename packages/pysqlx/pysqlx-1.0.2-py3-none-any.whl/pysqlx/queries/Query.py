

class Query:

    def __init__(self, client):
        self.__client = client

    def execute(self, param_tuple=None):
        return self.__client.execute(
            query=self,
            param_tuple=param_tuple
        )

    def execute_many(self, param_tuple_list):
        return self.__client.execute_many(
            query=self,
            param_tuple_list=param_tuple_list
        )
