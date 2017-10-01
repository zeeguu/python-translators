import asyncio
import threading
import time

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import merge_translations
from python_translators.translators.composite_translator import CompositeTranslator
from python_translators.utils import current_milli_time
from python_translators.translators.composite_translator import translate_worker


def join_threads(threads: [threading.Thread], timeout_ms=None) -> None:
    assert timeout_ms is None or timeout_ms >= 0

    if timeout_ms is None:
        [t.join() for t in threads]
    else:
        start_time = current_milli_time()

        idx = 0

        while current_milli_time() - start_time < timeout_ms and idx < len(threads):
            if not threads[idx].is_alive():
                idx += 1

            time.sleep(0.01)


class CompositeParallelTranslator(CompositeTranslator):
    def __init__(self, source_language: str, target_language: str, translators: [Translator] = None):
        super(CompositeParallelTranslator, self).__init__(source_language, target_language, translators)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        responses = [None] * len(self.translators)
        threads = []

        # Start a thread for each translator
        for idx, translator in enumerate(self.translators):
            translate_thread = threading.Thread(target=translate_worker, args=(translator, query, responses, idx))
            translate_thread.start()
            threads.append(translate_thread)

        # Wait for all threads to complete
        if query.budget_is_unconstrained():
            join_threads(threads)
        else:
            join_threads(threads, timeout_ms=query.budget.time)

        translations = []
        money_costs = 0

        # Process all the responses
        for idx, resp in enumerate(responses):
            if not threads[idx].is_alive():
                translations = merge_translations(translations, resp.translations)
                money_costs += resp.costs.money

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=money_costs
            )
        )

    def get_translator_name(self):
        return 'CompositeParallel(' + self.translator_list_text() + ')'
