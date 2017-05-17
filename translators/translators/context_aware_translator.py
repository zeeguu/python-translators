from abc import ABCMeta, abstractmethod

from translators.translator import Translator
from translators.context_processors.context_processor import ContextProcessor


class ContextAwareTranslator(Translator, metaclass=ABCMeta):
    def __init__(self, source_language: str, target_language: str) -> None:
        super(ContextAwareTranslator, self).__init__(source_language, target_language)

        self.context_processors = []

    @abstractmethod
    def _ca_translate(self, query: str, before_context: str, after_context: str, max_translations: int = 1) -> [str]:
        pass

    def ca_translate(self, query: str, before_context: str, after_context: str, max_translations: int = 1) -> [str]:

        params = {
            'before_context': before_context,
            'query': query,
            'after_context': after_context
        }

        # Pass params through all the context processors
        for context_processor in self.context_processors:
            params = context_processor.process_context(**params)

        # Add `max_translations` to the new dict of params
        params['max_translations'] = max_translations

        return self._ca_translate(**params)

    def add_context_processor(self, context_processor: ContextProcessor) -> None:
        self.context_processors.append(context_processor)
