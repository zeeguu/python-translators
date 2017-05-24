from abc import ABCMeta, abstractmethod
from collections import deque

from python_translators.translators.translator import Translator
from python_translators.context_processors.context_processor import ContextProcessor
from python_translators.utils import current_milli_time
from python_translators.translation_processors.translation_processor import TranslationProcessor
from python_translators.translation_request import TranslationRequest

MAX_MEASUREMENTS = 100


class ContextAwareTranslator(Translator, metaclass=ABCMeta):
    def __init__(self, source_language: str, target_language: str) -> None:
        super(ContextAwareTranslator, self).__init__(source_language, target_language)

        self.context_processors = []
        self.translation_processors = []
        self.time_expenses = deque([], MAX_MEASUREMENTS)  # only track the last MAX_MEASUREMENTS translations

    @abstractmethod
    def _ca_translate(self, query: str, before_context: str, after_context: str, max_translations: int = 1) -> [str]:
        pass

    def ca_translate(self, query: str, before_context: str, after_context: str, max_translations: int = 1) -> [str]:
        """
        Performs a context aware translation
        
        :param query: What has to be translated
        :param before_context: The context that occurs before the query
        :param after_context: The context that occurs after the query
        :param max_translations: The maxin number of translations
        :return: 
        """
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

        start_time = current_milli_time()  # start the timer
        translations = self._ca_translate(**params)  # translate request
        end_time = current_milli_time()  # end the timer

        self.time_expenses.append(end_time - start_time)

        return translations

    def estimate_time_expense(self, request : TranslationRequest = None):
        """
        Estimates the cost in time to translate the given request.
        
        :param request: 
        :return: time in milliseconds
        """
        if len(self.time_expenses) == 0:
            return 20  # If nothing has been measured yet, default to 20

        # Return the average
        return sum(self.time_expenses) / len(self.time_expenses)

    def add_context_processor(self, context_processor: ContextProcessor) -> None:
        """
        
        :param context_processor: 
        :return: 
        """
        self.context_processors.append(context_processor)

    def add_translation_processor(self, translation_processor: TranslationProcessor) -> None:
        self.translation_processors.append(translation_processor)
