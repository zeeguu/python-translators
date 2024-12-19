import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery
from python_translators.translators.wordnik_translator import WordnikTranslator
from python_translators.config import get_key_from_config


class TestWordnikTranslator(TestCase):

    def setUp(self):
        self.translator = WordnikTranslator(
            source_language="es",
            target_language="en",
            key=get_key_from_config("WORDNIK_API_KEY"),
        )

    def testUppercaseMatters(self):
        response = self.translator.translate(
            TranslationQuery(query="March", max_translations=5)
        )
        response2 = self.translator.translate(
            TranslationQuery(query="march", max_translations=5)
        )

        # The first is the month; the second is the verb
        assert response.translations != response2.translations
