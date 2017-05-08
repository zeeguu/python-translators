from abc import ABCMeta, abstractmethod

from translator import Translator


class ContextAwareTranslator(Translator):
    __metaclass__ = ABCMeta

    def __init__(self, source_language, target_language):
        super(ContextAwareTranslator, self).__init__(source_language, target_language)

        self.context_processors = []

    @abstractmethod
    def ca_translate(self, query, before_context, after_context, max_translations=1):
        pass

    def add_context_processor(self, context_processor):
        self.context_processors.append(context_processor)
