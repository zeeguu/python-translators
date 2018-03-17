from unittest import TestCase

from python_translators.translation_query import TranslationQuery
from python_translators.translators.best_effort_translator import DummyBestEffortTranslator


class TestBestEffortTranslator(TestCase):

    def setUp(self):
        self.translator = DummyBestEffortTranslator(source_language='es', target_language='en')

    def testEnsureDifferentWordThanOriginalReturnedIfPossible(self):
        response = self.translator.translate(TranslationQuery(
            query="ada",
            max_translations=1
        ))

        self.assertNotEqual(response.translations[0]['translation'], 'ada')
