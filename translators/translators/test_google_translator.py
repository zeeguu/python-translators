import os
from unittest import TestCase
from configobj import ConfigObj
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):

    def setUp(self):
        self.translator = GoogleTranslator ()

    def testSimple(self):

        translation = self.translator.ca_translate('De directeur', 'treedt', 'af', 'nl', 'en')
        assert translation == u"resigns"

        translation = self.translator.ca_translate('Dark', 'matter', 'is to be found in the universe', 'en', 'nl')
        assert translation == "materie"

    def testSpanish(self):

        translation = self.translator.ca_translate('Estoy en la', 'cama', '', 'es', 'en')
        assert translation == "bed"

    def testSuffixIsSimple(self):

        translation = self.translator.ca_translate('Estoy en la', 'cama', ', e soy dormiendo', 'es', 'en')
        assert translation == "bed"