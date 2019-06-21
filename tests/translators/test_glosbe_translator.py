import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery


class TestGlosbeTranslator(TestCase):

    def setUp(self):
        self.translator = GlosbeTranslator(source_language='es', target_language='en')

    # NOTE: Test disabled since Glosbe seems to not work at the moment
    def _testNumberOfTranslationsWorks(self):

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=5
        ))

        self.assertIn('bed', [each['translation'] for each in response.translations])
        self.assertEqual(len(response.translations), 5)

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=3
        ))

        self.assertEqual(response.translations[0]['translation'], 'bed')
        self.assertEqual(len(response.translations), 3)

    # NOTE: Test disabled since Glosbe seems to not work at the moment
    def _test_en2en(self):

        self.translator = GlosbeTranslator(source_language='en', target_language='en')

        response = self.translator.translate(TranslationQuery(
            query="mogul",
            max_translations=20
        ))

        self.assertIn("A wealthy and powerful business person", [each['translation'] for each in response.translations])

    # NOTE: Test disabled since Glosbe seems to not work at the moment
    def _test_de2de(self):

        self.translator = GlosbeTranslator(source_language='de', target_language='de')

        response = self.translator.translate(TranslationQuery(
            query="Wunder",
            max_translations=20
        ))

        self.assertIn("Mirakel", [each['translation'] for each in response.translations])

if __name__ == '__main__':
    unittest.main()
