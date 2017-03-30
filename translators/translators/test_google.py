# -*- coding: utf8 -*-
from unittest import TestCase
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):

    def setUp(self):
        self.goog = GoogleTranslator ()

    def testContextMatters(self):

        translation1 = self.goog.ca_translate('treedt', 'nl', 'en', 'De directeur', 'af')
        translation2 = self.goog.ca_translate('matter', 'en', 'nl', 'Dark', 'is to be found in the universe')

        assert translation1 == "resigns"
        assert translation2 == "materie"

    def testSuffixIsEmpty(self):

        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', '')
        assert translation == "bed"

    def testUnicodeCharactersInContext(self):

        translation = self.goog.ca_translate( 'klein', 'de', 'en', u'Ein', u'jäger' )
        assert translation == "small"

    def testUnicodeCharactersInWordToTranslate(self):

        translation = self.goog.ca_translate(u'jäger', 'de', 'en', u'Die jäggendlich ', u' geht zum jäggen' )
        assert translation == "hunter"

    def testUnicodeInResult(self):
        translation = self.goog.ca_translate('hunter', 'en', 'de', u'The ', u' goes hunting.' )
        assert translation == u'Jäger'

    def testSuffixStartsWithPunctuation(self):

        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ', e soy dormiendo')
        assert translation == "bed"

        # the problem appears even when the right_context begins with a space
        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ' , e soy dormiendo')
        assert translation == "bed"
