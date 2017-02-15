from abc import ABCMeta, abstractmethod

from translator import Translator


class ContextAwareTranslator(Translator):
    __metaclass__ = ABCMeta

    @abstractmethod
    def ca_translate(self, left_context, query, right_context, from_language, to_language, max_translations=1):
        pass
