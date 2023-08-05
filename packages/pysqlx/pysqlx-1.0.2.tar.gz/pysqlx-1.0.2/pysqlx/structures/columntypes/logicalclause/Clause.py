

from abc import ABC, abstractmethod


class Clause(ABC):

    def __init__(self):
        super().__init__()

    def __and__(self, other):
        from .And import And
        return And(clause0=self, clause1=other)

    def __or__(self, other):
        from .Or import Or
        return Or(clause0=self, clause1=other)

    def __invert__(self):
        return self.get_not_clause()

    @abstractmethod
    def get_not_clause(self):
        pass
