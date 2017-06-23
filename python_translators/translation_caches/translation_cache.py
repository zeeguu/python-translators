from abc import ABCMeta, abstractmethod

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse


class TranslationCache(object, metaclass=ABCMeta):

    def __init__(self, translator_type: str):
        self.translator_type = translator_type

    def get_translator_type(self):
        return self.translator_type

    @abstractmethod
    def store(self, query: TranslationQuery, source_language: str, target_language: str,
              translations: [dict]) -> None:
        pass

    @abstractmethod
    def fetch(self, query: TranslationQuery, source_language: str, target_language: str) -> [dict]:
        pass
