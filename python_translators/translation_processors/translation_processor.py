from abc import ABCMeta, abstractmethod


class TranslationProcessor(metaclass=ABCMeta):

    @abstractmethod
    def translation(self, translation, original_request):
        pass
