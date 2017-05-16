# -*- coding: utf8 -*-
import unittest
from unittest import TestCase
from translators import MicrosoftTranslator


class TestMicrosoftTranslator(TestCase):
    def setUp(self):
        self.translators = {
            'en-nl': MicrosoftTranslator('en', 'nl'),
            'nl-en': MicrosoftTranslator('nl', 'en'),
            'es-en': MicrosoftTranslator('es', 'en'),
            'de-en': MicrosoftTranslator('de', 'en'),
            'en-de': MicrosoftTranslator('en', 'de'),
        }

    def test_simple_translations(self):
        translation = self.translators['en-nl'].translate(query='hello')

        self.assertEqual(translation[0], 'Hallo')

        translation = self.translators['nl-en'].translate(query='De boom is groen')

        self.assertEqual(translation[0], 'The tree is green')

    def test_invalid_microsoft_key(self):
        self.assertRaises(Exception, MicrosoftTranslator, '<this is an invalid key>')

    def test_ca_translations(self):

        translation = self.translators['nl-en'].ca_translate(
            before_context='De directeur',
            query='treedt af',
            after_context='')

        self.assertEqual(translation[0], 'resigns')

        translation = self.translators['en-nl'].ca_translate(
            before_context='Dark',
            query='matter',
            after_context='is an unidentified type of matter distinct from dark energy.')

        self.assertEqual(translation[0], 'materie')

    def test_unicode_outputs(self):
        translation = self.translators['en-de'].ca_translate(
            before_context='The ',
            query='lion',
            after_context='goes to the forest')

        self.assertEqual(translation[0], u'Löwe')

    def test_unicode_inputs(self):
        translation = self.translators['de-en'].translate(query=u'Löwe')

        self.assertEqual(translation[0], 'Lion')

if __name__ == '__main__':
    unittest.main()
