from abc import ABCMeta, abstractmethod
from collections import deque
import copy
import statistics

from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.response_processors.response_processor import ResponseProcessor
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import TranslationResponse
from python_translators.translation_query import TranslationQuery
from python_translators.utils import current_milli_time, format_dict_for_logging
from python_translators.stat_tracker import StatTracker
from python_translators import logger
from python_translators.translation_caches.translation_cache import TranslationCache

N_TIME_ELEMENTS = 100

REQUEST_ACCEPTANCE_PROBABILITY = 0.95
MIN_ACCEPTANCE_ENTRIES = 15


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

        self.cache: TranslationCache = None

        self.time_expense_tracker = StatTracker(max_elements=1000)

    @abstractmethod
    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        pass

    @abstractmethod
    def compute_money_costs(self, query: TranslationQuery) -> float:
        pass

    def _should_reject_request(self, query: TranslationQuery) -> bool:
        if query.budget_is_unconstrained():
            return False

        if self.time_expense_tracker.size() > MIN_ACCEPTANCE_ENTRIES and \
           self.time_expense_tracker.probability_of_being_lower(query.budget.time) < REQUEST_ACCEPTANCE_PROBABILITY:
            return True

        if self.estimate_costs(query).money > query.budget.money:
            return True

        return False

    def translate(self, query: TranslationQuery) -> TranslationResponse:
        start_time = current_milli_time()

        if self._should_reject_request(query):
            return TranslationResponse(
                translations=[],
                costs=TranslationCosts(
                    time=current_milli_time() - start_time
                )
            )

        if self.cache:
            results = self.cache.fetch(
                query=query,
                source_language=self.source_language,
                target_language=self.target_language)

            if results:
                time_passed = current_milli_time() - start_time

                logger.info(format_dict_for_logging(dict(
                    EVENT='translation_result',
                    FROM_CACHE=True,
                    TIME_PASSED=time_passed,

                    TRANSLATOR_NAME=self.get_translator_name(),

                    # The query
                    QUERY='\'' + query.query + '\'',
                    BEFORE_CONTEXT='\'' + query.before_context + '\'',
                    PRE_AFTER_CONTEXT='\'' + query.after_context + '\'',

                    TRANSLATIONS=[r['translation'] for r in results],
                    QUALITIES=[r['quality'] for r in results],
                    SERVICE_NAMES=[r['service_name'] for r in results],
                )))

                self.time_expense_tracker.track(time_passed)

                return TranslationResponse(
                    translations=results,
                    costs=TranslationCosts(
                        money=0,
                        time=current_milli_time() - start_time
                    )
                )

        before_pre_processing = copy.copy(query)

        # Pre-processing
        for query_processor in self.query_processors:
            query = query_processor.process_query(query)

        # try/catch added to fix issue #36 (https://github.com/zeeguu-ecosystem/Python-Translators/issues/36)
        try:
            translation_response = self._translate(query)
        except Exception as e:
            logger.info(f"Exception raised: {e}")
            logger.info(f"Translator {self.get_translator_name()} failed in _translate()")
            return TranslationResponse(
                translations=[],
                costs=TranslationCosts(
                    time=current_milli_time() - start_time
                )
            )

        # Post-processing
        for response_processor in self.response_processors:
            translation_response = response_processor.process_response(translation_response)

        time_passed = current_milli_time() - start_time

        log_string = format_dict_for_logging(dict(
            EVENT='translation_result',
            FROM_CACHE=False,
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
        ))
        logger.info(log_string)

        # Store time costs in response
        translation_response.costs.time = time_passed

        self.time_expense_tracker.track(time_passed)

        if self.cache:
            self.cache.store(
                query=before_pre_processing,
                source_language=self.source_language,
                target_language=self.target_language,
                translations=translation_response.translations
            )

        return translation_response

    def get_time_expense_tracker(self):
        return self.time_expense_tracker

    def add_query_processor(self, query_processor: QueryProcessor) -> None:
        self.query_processors.append(query_processor)

    def add_response_processor(self, response_processor: ResponseProcessor) -> None:
        self.response_processors.append(response_processor)

    def get_quality(self):
        return self.quality

    def get_service_name(self):
        return self.service_name

    def get_translator_name(self):
        return self.translator_name

    def make_translation(self, translation, quality=None):
        if quality:
            _quality = quality
        else:
            _quality = self.get_quality()

        return dict(
            translation=translation,
            service_name=self.get_service_name(),
            quality=_quality
        )

    def set_cache(self, cache: TranslationCache):
        self.cache = cache

    def estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        costs = TranslationCosts()
        costs.money = self.compute_money_costs(query=query)
        costs.time = self.time_expense_tracker.mean(default=100)

        return costs
