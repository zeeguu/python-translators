from unittest import TestCase
import time

from python_translators.translators.composite_parallel_translator import CompositeParallelTranslator
from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery, TranslationBudget
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts


class UnresponsiveTranslator(Translator):
    def __init__(self):
        super(UnresponsiveTranslator, self).__init__(
            source_language='nl',
            target_language='en',
            translator_name='unresponsive_translator',
            quality=0,
            service_name='Unknown')

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        time.sleep(5_000_000) # very unresponsive translator
        return TranslationResponse(
            costs=TranslationCosts(
                time=5_000_000,
                money=0.001
            ),
            translations=[]
        )

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        return TranslationCosts(
            money=0.001  # not important
        )


class TestParallelTranslator(TestCase):

    def test_unresponsive_translator(self):
        t = UnresponsiveTranslator()

        ct = CompositeParallelTranslator(source_language='nl', target_language='en')
        ct.add_translator(t)

        translations = ct.translate(TranslationQuery(
            query='boom',
            budget=TranslationBudget(
                time=2500  # 2.5 seconds
            )
        ))

        print(translations)
