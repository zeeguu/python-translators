import unittest
from unittest import TestCase
from translators import CollinsTranslator


class TestCollinsTranslator(TestCase):

    def setUp(self):
        self.translator = CollinsTranslator(source_language='nl', target_language='en')

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

if __name__ == '__main__':
    unittest.main()
