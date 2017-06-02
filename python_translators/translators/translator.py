from abc import ABCMeta, abstractmethod
from collections import deque

from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.response_processors.response_processor import ResponseProcessor
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import TranslationResponse
from python_translators.translation_query import TranslationQuery
from python_translators.utils import current_milli_time


class Translator(object, metaclass=ABCMeta):

    def __init__(self, source_language: str, target_language: str) -> None:
        self.source_language = source_language
        self.target_language = target_language

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

        # Pre-processing
        for query_processor in self.query_processors:
            query = query_processor.process_query(query)

        start_time = current_milli_time()
        translation_response = self._translate(query)
        time_passed = current_milli_time() - start_time

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

    def estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        costs = self._estimate_costs(query)

        # set the time costs
        costs.time = sum(self.time_expenses) / len(self.time_expenses)

        return costs
