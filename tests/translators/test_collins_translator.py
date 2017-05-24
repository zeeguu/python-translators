import unittest
from unittest import TestCase
from python_translators.translators.collins_translator import CollinsTranslator
from python_translators.translation_query import TranslationQuery


class TestCollinsTranslator(TestCase):
    def setUp(self):
        self.translator = CollinsTranslator(source_language='en', target_language='es')

    def test_invalid_source_language(self):

        # Dutch is not supported as a source language
        self.assertRaises(Exception,
                          CollinsTranslator.translate,
                          self.translator,
                          query='hallo')

    def test_invalid_destination_language(self):
        # Collins API can not translate Spanish to Dutch
        self.assertRaises(Exception,
                          CollinsTranslator.translate,
                          self.translator,
                          query='hola')

    def test_translation(self):

        self.translator.translate(TranslationQuery(
            query='boom'
        ))


if __name__ == '__main__':
    unittest.main()
