# -*- coding: utf8 -*-
from unittest import TestCase
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):
    def setUp(self):
        self.goog = GoogleTranslator().unique_instance()

    def testContextMatters(self):
        translation1 = self.goog.ca_translate('matter', 'en', 'nl', 'Dark', 'is to be found in the universe')

        self.assertEqual(translation1, 'materie')

    def testSuffixIsEmpty(self):
        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', '')
        self.assertEqual(translation, 'bed')

    def testUnicodeCharactersInContext(self):
        translation = self.goog.ca_translate('klein', 'de', 'en', u'Ein', u'löwe')
        self.assertEqual(translation, "small")

    def testUnicodeCharactersInWordToTranslate(self):
        translation = self.goog.ca_translate(u'löwen', 'de', 'en', u'Die schön', u' geht zum Wald')
        self.assertIn(translation, ['lion', 'beautiful lion'])

    def testUnicodeInResult(self):
        translation = self.goog.ca_translate('lion', 'en', 'de', 'The ', ' goes to the forrest.')
        self.assertEqual(translation, u'Löwe')

    def testSuffixStartsWithPunctuation(self):
        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ', e soy dormiendo')
        self.assertEqual(translation, 'bed')

        # the problem appears even when the right_context begins with a space
        translation = self.goog.ca_translate('cama', 'es', 'en', 'Estoy en la', ' , e soy dormiendo')
        self.assertEqual(translation, 'bed')

    def testQueryEndsWithPunctuation(self):
        translation = self.goog.ca_translate(before_context='Estoy en la',
                                             query='cama,',
                                             after_context=' e soy dormiendo',
                                             source_language='es',
                                             target_language='en')

        self.assertIn(translation, ['bed,', 'bed'])

    def test_strange_span_in_return(self):
        translation = self.goog.ca_translate(before_context='Ich hatte mich',
                                             query='eigentlich schon',
                                             after_context=' mit dem 1:1-Unentschieden abgefunden',
                                             source_language='de',
                                             target_language='en')

        assert "</span>" not in translation

    def test_escaped_characters_in_translation(self):
        translation = self.goog.ca_translate(
            before_context=u'Um Fernbusse aus dem Geschäft zu drängen, hat das Unternehmen damit begonnen, das',
            query='konzerneigene Flaggschiff',
            after_context=u'ICE straßentauglich zu machen. ',
            source_language='de',
            target_language='en')

        self.assertNotIn('&#39;', translation)

