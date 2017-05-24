from abc import ABCMeta, abstractmethod

from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.translation_query import TranslationQuery


class Translator(object, metaclass=ABCMeta):
    def __init__(self, source_language: str, target_language: str) -> None:
        self.source_language = source_language
        self.target_language = target_language

        self.query_processors = []

    @abstractmethod
    def _translate(self, query: TranslationQuery) -> [str]:
        pass

    def translate(self, query: TranslationQuery) -> [str]:

        for query_processor in self.query_processors:
            query = query_processor.process_query(query)

        return self._translate(query)

    def add_query_processor(self, query_processor: QueryProcessor):
        self.query_processors.append(query_processor)
