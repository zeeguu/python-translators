from unittest import TestCase
import time

from python_translators.translators.composite_parallel_translator import CompositeParallelTranslator
from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery, TranslationBudget
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.utils import current_milli_time


class UnresponsiveTranslator(Translator):
    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0

    def __init__(self):
        super(UnresponsiveTranslator, self).__init__(
            source_language='nl',
            target_language='en',
            translator_name='unresponsive_translator',
            quality=0,
            service_name='Unknown')

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        time.sleep(3) # very unresponsive translator
        return TranslationResponse(
            costs=TranslationCosts(
                time=3000,
                money=0.001
            ),
            translations=[]
        )


class TestParallelTranslator(TestCase):

    def test_unresponsive_translator(self):
        t = UnresponsiveTranslator()

        ct = CompositeParallelTranslator(source_language='nl', target_language='en')
        ct.add_translator(t)
        t1 = current_milli_time()

        translations = ct.translate(TranslationQuery(
            query='boom',
            budget=TranslationBudget(
                time=2500  # 2.5 seconds
            )
        ))

        t2 = current_milli_time()
        self.assertLess(t2 - t1 - 500, 2500)
