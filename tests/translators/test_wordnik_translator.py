import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery
from python_translators.translators.wordnik_translator import WordnikTranslator
from python_translators.utils import get_key_from_config


class TestWordniTranslator(TestCase):

    def setUp(self):
        self.translator = WordnikTranslator(source_language='es',
                                            target_language='en',
                                            key=get_key_from_config('WORDNIK_API_KEY'))

    def testNumberOfTranslationsWorks(self):
        response = self.translator.translate(TranslationQuery(
            query="conjunction",
            max_translations=5
        ))

        assert 2 <= len(response.translations)

