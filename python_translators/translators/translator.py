from abc import ABCMeta, abstractmethod


class Translator(object, metaclass=ABCMeta):
    def __init__(self, source_language: str, target_language: str) -> None:
        self.source_language = source_language
        self.target_language = target_language

    @abstractmethod
    def _translate(self, query: str, max_translations: int = 1) -> [str]:
        pass

    def translate(self, query: str, max_translations: int = 1) -> [str]:
        return self._translate(query, max_translations)


