

class Structure:

    def __init__(self, structure_name):
        self.__structure_name = structure_name

    @property
    def structure_name(self):
        return self.__structure_name
