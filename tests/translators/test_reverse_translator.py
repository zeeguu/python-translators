import unittest
from unittest import TestCase
from python_translators.translation_query import TranslationQuery
from translators.reverse_translator import ReverseTranslator


class TestReverseTranslator(TestCase):

    def setUp(self):
        self.translator = ReverseTranslator(source_language='es', target_language='en')

    def testNumberOfTranslationsWorks(self):

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=3
        ))

        self.assertEqual(response.translations[0]['translation'], 'amac')
        self.assertEqual(len(response.translations), 3)

        response = self.translator.translate(TranslationQuery(
            query="cama",
            max_translations=2
        ))

        self.assertEqual(response.translations[0]['translation'], 'amac')
        self.assertEqual(len(response.translations), 2)


if __name__ == '__main__':
    unittest.main()
