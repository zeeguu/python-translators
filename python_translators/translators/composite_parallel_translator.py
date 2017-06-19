import asyncio
import threading

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import merge_translations
from python_translators.translators.composite_translator import CompositeTranslator


def translate_worker(translator: Translator, query: TranslationQuery, responses: [TranslationResponse], idx: int):
    responses[idx] = translator.translate(query)


class CompositeParallelTranslator(CompositeTranslator):
    def __init__(self, source_language: str, target_language: str, translators: [Translator] = None):
        super(CompositeParallelTranslator, self).__init__(source_language, target_language, translators)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        responses = [None] * len(self.translators)
        threads = []

        # Start a thread for each translator
        for idx, translator in enumerate(self.translators):
            t = threading.Thread(target=translate_worker, args=(translator, query, responses, idx))
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        translations = []
        money_costs = 0

        # Process all the responses
        for resp in responses:
            translations = merge_translations(translations, resp.translations)
            money_costs += resp.costs.money

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=money_costs
            )
        )
