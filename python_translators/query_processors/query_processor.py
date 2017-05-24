from abc import ABCMeta, abstractmethod
from python_translators.translation_query import TranslationQuery


class QueryProcessor(object, metaclass=ABCMeta):

    @abstractmethod
    def process_query(self, query: TranslationQuery) -> TranslationQuery:
        """
        
        :param query: 
        :return: 
        """
        pass
