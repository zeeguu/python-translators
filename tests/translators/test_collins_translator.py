import unittest
from unittest import TestCase
from translators import CollinsTranslator


class TestCollinsTranslator(TestCase):

    def setUp(self):
        self.translator = CollinsTranslator()

    def test_invalid_source_language(self):

        # Dutch is not supported as a source language
        self.assertRaises(Exception,
                          CollinsTranslator.translate,
                          self.translator,
                          query='hallo',
                          source_language='nl',
                          target_language='en')

    def test_invalid_destination_language(self):
        self.assertRaises(Exception,
                          CollinsTranslator.translate,
                          self.translator,
                          query='hola',
                          source_language='es',
                          target_language='nl')


if __name__ == '__main__':
    unittest.main()
