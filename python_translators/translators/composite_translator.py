import threading
import time

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import merge_responses
from python_translators.utils import current_milli_time


def translate_worker(translator: Translator, query: TranslationQuery, responses: [TranslationResponse], idx: int):
    responses[idx] = translator.translate(query)


class CompositeTranslator(Translator):
    def compute_money_costs(self, query: TranslationQuery) -> float:
        return sum(translator.compute_money_costs(query) for translator in self.translators)

    def __init__(self, source_language: str, target_language: str, translators: [Translator] = None) -> None:
        super(CompositeTranslator, self).__init__(source_language, target_language)

        if not translators:
            self.translators: [Translator] = []
        else:
            self.translators: [Translator] = translators

            # Make sure the source and target languages match the source and target languages
            # of the CompositeTranslator
            for t in translators:
                assert t.source_language == source_language
                assert t.target_language == target_language

    def get_translator_name(self):
        return 'Composite(' + self.translator_list_text() + ')'

    def add_translator(self, translator: Translator):
        assert translator.source_language == self.source_language
        assert translator.target_language == self.target_language

        self.translators.append(translator)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        responses = [None] * len(self.translators)

        t_start = current_milli_time()
        initial_time_budget = query.budget.time
        # print('budget', initial_time_budget)

        for idx, translator in enumerate(self.translators):
            # Start a thread for each translator
            translate_thread = threading.Thread(target=translate_worker, args=(translator, query, responses, idx))
            translate_thread.start()

            while translate_thread.is_alive() and current_milli_time() - t_start < initial_time_budget:
                time.sleep(0.05)

            # print('cmt - start', current_milli_time() - t_start)

            if translate_thread.is_alive():
                break

            query.budget.subtract_time(current_milli_time() - t_start)

        responses = [t.translate(query) for t in self.translators]

        return merge_responses(responses)

    def translator_list_text(self):
        return ', '.join(map(lambda t: t.get_translator_name(), self.translators))
