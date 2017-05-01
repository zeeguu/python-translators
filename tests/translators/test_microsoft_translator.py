# -*- coding: utf8 -*-
from unittest import TestCase
from translators import MicrosoftTranslator


class TestGoogleTranslator(TestCase):
    def setUp(self):
        self.translator = MicrosoftTranslator.unique_instance()

    def test_simple_translations(self):
        translation = self.translator.translate(
            query='hello',
            source_language='en',
            target_language='nl',
        )

        self.assertEquals(translation, 'Hallo')

        translation = self.translator.translate(
            query='De boom is groen',
            source_language='nl',
            target_language='en'
        )

        self.assertEquals(translation, 'The tree is green')

    def test_invalid_microsoft_key(self):

        self.assertRaises(Exception, MicrosoftTranslator, '<this is an invalid key>')
