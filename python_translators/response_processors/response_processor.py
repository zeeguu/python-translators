from abc import ABCMeta, abstractmethod
from python_translators.translation_response import TranslationResponse


class ResponseProcessor(object, metaclass=ABCMeta):

    @abstractmethod
    def process_response(self, response: TranslationResponse) -> TranslationResponse:
        pass
