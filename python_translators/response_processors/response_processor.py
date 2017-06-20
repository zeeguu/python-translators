from abc import ABCMeta, abstractmethod
from python_translators.translation_response import TranslationResponse


class ResponseProcessor(object, metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def process_response(self, response: TranslationResponse) -> TranslationResponse:
        pass

    def get_name(self):
        return self.name
