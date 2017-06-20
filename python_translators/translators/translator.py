from abc import ABCMeta, abstractmethod
from collections import deque
import copy

from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.response_processors.response_processor import ResponseProcessor
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import TranslationResponse
from python_translators.translation_query import TranslationQuery
from python_translators.utils import current_milli_time, format_dict_for_logging
from python_translators import logger


class Translator(object, metaclass=ABCMeta):
    def __init__(self,
                 source_language: str,
                 target_language: str,
                 translator_name: str = None,
                 quality: int = None,
                 service_name: str = None) -> None:

        self.source_language = source_language
        self.target_language = target_language
        self.quality = quality
        self.service_name = service_name
        self.translator_name = translator_name

        self.query_processors = []
        self.response_processors = []

        self.time_expenses = deque([], maxlen=1000)  # deque will store recent time expenses

    @abstractmethod
    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        pass

    @abstractmethod
    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        pass

    def translate(self, query: TranslationQuery) -> TranslationResponse:

        before_pre_processing = copy.copy(query)

        # Pre-processing
        for query_processor in self.query_processors:
            query = query_processor.process_query(query)

        start_time = current_milli_time()

        translation_response = self._translate(query)
        time_passed = current_milli_time() - start_time

        logger.info(format_dict_for_logging(dict(
            EVENT='translation_result',
            TIME_PASSED=time_passed,

            TRANSLATOR_NAME=self.get_translator_name(),

            CONTEXT_PROCESSORS=list(map(lambda qp: qp.get_name(), self.query_processors)),
            RESPONSE_PROCESSORS=list(map(lambda rp: rp.get_name(), self.response_processors)),

            # Before pre-processing
            PRE_QUERY='\'' + before_pre_processing.query + '\'',
            PRE_BEFORE_CONTEXT='\'' + before_pre_processing.before_context + '\'',
            PRE_AFTER_CONTEXT='\'' + before_pre_processing.after_context + '\'',

            # After pre-processing
            POST_QUERY='\'' + query.query + '\'',
            POST_BEFORE_CONTEXT='\'' + query.before_context + '\'',
            POST_AFTER_CONTEXT='\'' + query.after_context + '\'',

            TRANSLATIONS=translation_response.get_raw_translations(),
            QUALITIES=translation_response.get_raw_qualities(),
            SERVICE_NAMES=translation_response.get_raw_service_names(),
        )))

        # Post-processing
        for response_processor in self.response_processors:
            translation_response = response_processor.process_response(translation_response)

        # Store time costs in response
        translation_response.costs.time = time_passed

        # Store time expense in history deque
        self.time_expenses.append(time_passed)

        return translation_response

    def add_query_processor(self, query_processor: QueryProcessor) -> None:
        self.query_processors.append(query_processor)

    def add_response_processor(self, response_processor: ResponseProcessor) -> None:
        self.response_processors.append(response_processor)

    def _average_time_costs(self):
        if not self.time_expenses:
            return 60  # if nothing has been measured yet, return (arbitrary) 60 ms

        return sum(self.time_expenses) / len(self.time_expenses)

    def get_quality(self):
        return self.quality

    def get_service_name(self):
        return self.service_name

    def get_translator_name(self):
        return self.translator_name

    def make_translation(self, translation):
        return dict(
            translation=translation,
            service_name=self.get_service_name(),
            quality=self.get_quality()
        )

    def estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        costs = self._estimate_costs(query)

        # set the time costs
        costs.time = sum(self.time_expenses) / len(self.time_expenses)

        return costs
