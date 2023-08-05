

from abc import ABC, abstractmethod


class IDialect(ABC):

    def __init__(self, dialect_name):
        self.__dialect_name = dialect_name

    @property
    def dialect_name(self):
        return self.__dialect_name

    @abstractmethod
    def get_table_qualifier(self, table):
        pass

    @abstractmethod
    def get_column_qualifier(self, column):
        pass

    @abstractmethod
    def get_DatetimeColumn_declaration(self, column):
        pass

    @abstractmethod
    def get_FloatColumn_declaration(self, column):
        pass

    @abstractmethod
    def get_IntegerColumn_declaration(self, column):
        pass

    @abstractmethod
    def get_TextColumn_declaration(self, column):
        pass

    def get_column_declaration(self, column):
        return getattr(
            self,
            'get_' + type(column).__name__ + '_declaration'
        )(column)

    @abstractmethod
    def get_Equal_string(self, clause):
        pass

    @abstractmethod
    def get_GreaterThan_string(self, clause):
        pass

    @abstractmethod
    def get_GreaterThanEqual_string(self, clause):
        pass

    @abstractmethod
    def get_InList_string(self, clause):
        pass

    @abstractmethod
    def get_IsNotNull_string(self, clause):
        pass

    @abstractmethod
    def get_IsNull_string(self, clause):
        pass

    @abstractmethod
    def get_LessThan_string(self, clause):
        pass

    @abstractmethod
    def get_LessThanEqual_string(self, clause):
        pass

    @abstractmethod
    def get_Like_string(self, clause):
        pass

    @abstractmethod
    def get_NotBetween_string(self, clause):
        pass

    @abstractmethod
    def get_NotEqual_string(self, clause):
        pass

    @abstractmethod
    def get_NotInList_string(self, clause):
        pass

    @abstractmethod
    def get_NotLike_string(self, clause):
        pass

    @abstractmethod
    def get_Or_string(self, clause):
        pass

    def get_clause_string(self, clause):
        return getattr(
            self,
            'get_' + type(clause).__name__ + '_string'
        )(clause)

    @abstractmethod
    def get_Create_database_string(self, query):
        pass

    @abstractmethod
    def get_Create_schema_string(self, query):
        pass

    @abstractmethod
    def get_Create_table_string(self, query):
        pass

    def get_Create_string(self, query):
        return getattr(
            self,
            'get_Create_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Delete_table_string(self, query):
        pass

    def get_Delete_string(self, query):
        return getattr(
            self,
            'get_Delete_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Drop_database_string(self, query):
        pass

    @abstractmethod
    def get_Drop_schema_string(self, query):
        pass

    @abstractmethod
    def get_Drop_table_string(self, query):
        pass

    def get_Drop_string(self, query):
        return getattr(
            self,
            'get_Drop_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_GetLength_table_string(self, query):
        pass

    def get_GetLength_string(self, query):
        return getattr(
            self,
            'get_GetLength_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Insert_table_string(self, query):
        pass

    def get_Insert_string(self, query):
        return getattr(
            self,
            'get_Insert_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_IsEmpty_table_string(self, query):
        pass

    def get_IsEmpty_string(self, query):
        return getattr(
            self,
            'get_IsEmpty_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_IsExists_database_string(self, query):
        pass

    @abstractmethod
    def get_IsExists_schema_string(self, query):
        pass

    @abstractmethod
    def get_IsExists_table_string(self, query):
        pass

    def get_IsExists_string(self, query):
        return getattr(
            self,
            'get_IsExists_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Select_table_string(self, query):
        pass

    def get_Select_string(self, query):
        return getattr(
            self,
            'get_Select_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_SelectDistinct_table_string(self, query):
        pass

    def get_SelectDistinct_string(self, query):
        return getattr(
            self,
            'get_SelectDistinct_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Truncate_table_string(self, query):
        pass

    def get_Truncate_string(self, query):
        return getattr(
            self,
            'get_Truncate_' + query.structure.structure_name + '_string'
        )(query)

    @abstractmethod
    def get_Union_table_string(self, query):
        pass

    def get_Union_string(self, query):
        return getattr(
            self,
            'get_Union_' + query.structure_list[0].structure_name + '_string'
        )(query)

    def get_query_string(self, query):
        return getattr(self, 'get_' + type(query).__name__ + '_string')(query)

    @abstractmethod
    def get_Update_table_string(self, query):
        pass

    def get_Update_string(self, query):
        return getattr(
            self,
            'get_Update_' + query.structure.structure_name + '_string'
        )(query)
