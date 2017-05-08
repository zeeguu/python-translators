from abc import ABCMeta, abstractmethod

from translator import Translator


class ContextAwareTranslator(Translator):
    __metaclass__ = ABCMeta

    def __init__(self, source_language, target_language):
        super(ContextAwareTranslator, self).__init__(source_language, target_language)

        self.context_processors = []

    @abstractmethod
    def _ca_translate(self, query, before_context, after_context, max_translations=1):
        pass

    def ca_translate(self, query, before_context, after_context, max_translations=1):
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

    def add_context_processor(self, context_processor):
        self.context_processors.append(context_processor)
