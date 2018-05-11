import unittest
from unittest import TestCase
from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery
from translators.glosbe_over_tor_translator import GlosbeOverTorTranslator


class TestGlosbeTranslator(TestCase):

    def setUp(self):
        self.translator = GlosbeOverTorTranslator(source_language='de', target_language='nl')

    def testNumberOfTranslationsWorks(self):

        response = self.translator.translate(TranslationQuery(
            query="genommen",
            max_translations=5
        ))

        print (response.translations)

        # self.assertEqual(response.translations[0]['translation'], 'bed')
        # self.assertEqual(len(response.translations), 5)



if __name__ == '__main__':
    unittest.main()
