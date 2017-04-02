# -*- coding: utf8 -*-
from unittest import TestCase
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):

    def setUp(self):
        self.goog = GoogleTranslator()

    def testContextMatters(self):

        translation1 = self.goog.ca_translate('treedt', 'nl', 'en', 'De directeur', 'af')
        translation2 = self.goog.ca_translate('matter', 'en', 'nl', 'Dark', 'is to be found in the universe')

        assert translation1 == "resigns"
        assert translation2 == "materie"

    def testSuffixIsEmpty(self):

        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', '')
        assert translation == "bed"

    def testUnicodeCharactersInContext(self):

        translation = self.goog.ca_translate( 'klein', 'de', 'en', u'Ein', u'löwe')
        assert translation == "small"

    def testUnicodeCharactersInWordToTranslate(self):

        translation = self.goog.ca_translate(u'löwen', 'de', 'en', u'Die schön', u' geht zum Wald')
        assert translation == "lion"

    def testUnicodeInResult(self):
        translation = self.goog.ca_translate('lion', 'en', 'de', 'The ', ' goes to the forrest.')
        assert translation == u'Löwe'

    def testSuffixStartsWithPunctuation(self):

        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ', e soy dormiendo')
        assert translation == "bed"

        # the problem appears even when the right_context begins with a space
        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ' , e soy dormiendo')
        assert translation == "bed"

    def testQueryEndsWithPunctuation(self):
        translation = self.goog.ca_translate(before_context='Estoy en la',
                                             query='cama,',
                                             after_context=' e soy dormiendo',
                                             source_language='es',
                                             target_language='en')

        assert translation == "bed,"

    def test_strange_span_in_return(self):

        translation = self.goog.ca_translate(before_context='Ich hatte mich',
                                             query='eigentlich schon',
                                             after_context=' mit dem 1:1-Unentschieden abgefunden',
                                             source_language='de',
                                             target_language='en')

        # print translation
        assert "</span>" not in translation
