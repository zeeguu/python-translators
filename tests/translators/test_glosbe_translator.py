import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery


class TestGlosbeTranslator(TestCase):

    def setUp(self):
        self.translator = GlosbeTranslator(source_language='es', target_language='en')

    def testNumberOfTranslationsWorks(self):

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=5
        ))

        self.assertEqual(response.translations[0]['translation'], 'bed')
        self.assertEqual(len(response.translations), 5)

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=3
        ))

        self.assertEqual(response.translations[0]['translation'], 'bed')
        self.assertEqual(len(response.translations), 3)


if __name__ == '__main__':
    unittest.main()
