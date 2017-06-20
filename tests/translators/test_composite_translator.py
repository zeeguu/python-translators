import unittest
from unittest import TestCase
from python_translators.translators.collins_translator import CollinsTranslator
from python_translators.translation_query import TranslationQuery
from python_translators.translators.composite_translator import CompositeTranslator
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translators.glosbe_translator import GlosbeTranslator
import warnings


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            test_func(self, *args, **kwargs)
    return do_test


class TestCollinsTranslator(TestCase):

    @ignore_warnings
    def setUp(self):
        self.translator = CompositeTranslator(source_language='nl', target_language='en')

        self.translator.add_translator(GoogleTranslatorFactory.build_with_context(source_language='nl', target_language='en'))
        self.translator.add_translator(GlosbeTranslator(source_language='nl', target_language='en'))

    @ignore_warnings
    def testBasicTranslation(self):
        response = self.translator.translate(TranslationQuery(
            query='boom'
        ))

if __name__ == '__main__':
    unittest.main()
