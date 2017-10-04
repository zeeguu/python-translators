from abc import ABCMeta, abstractmethod
from python_translators.translation_query import TranslationQuery


class QueryProcessor(object, metaclass=ABCMeta):

    def __init__(self, name: str):
        self.name = name

    def process_query(self, query: TranslationQuery) -> TranslationQuery:
        """
        
        :param query: 
        :return: 
        """
        pass

    def get_name(self):
        return self.name
