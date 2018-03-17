from unittest import TestCase

from python_translators.translation_query import TranslationQuery
from python_translators.translators.best_effort_translator import DummyBestEffortTranslator, BestEffortTranslator


class TestBestEffortTranslator(TestCase):

    def setUp(self):
        self.translator = DummyBestEffortTranslator(source_language='de', target_language='en')
        self.bet = BestEffortTranslator(source_language='de', target_language='en')

    def testEnsureDifferentWordThanOriginalReturnedIfPossible(self):
        response = self.translator.translate(TranslationQuery(
            query="ada",
            max_translations=1
        ))

        self.assertNotEqual(response.translations[0]['translation'], 'ada')

    def testEnsureContextualHasPriority(self):

        response = self.bet.translate(TranslationQuery(
            before_context='Hunderte Züge und Dutzende Flüge wurden ',
            query='gestrichen',
            after_context=' .',
            max_translations=3
        ))

        assert (response.translations[0]['translation'] == "canceled")
