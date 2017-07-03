# -*- coding: utf8 -*-
from unittest import TestCase
from python_translators.translation_query import TranslationQuery
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translators.translator import Translator


class TestGoogleTranslator(TestCase):
    def setUp(self):
        self.translators: [Translator] = {
            'en-nl': GoogleTranslatorFactory.build_with_context('en', 'nl'),
            'es-en': GoogleTranslatorFactory.build_with_context('es', 'en'),
            'de-en': GoogleTranslatorFactory.build_with_context('de', 'en'),
            'en-de': GoogleTranslatorFactory.build_with_context('en', 'de'),
            'nl-en': GoogleTranslatorFactory.build_with_context('nl', 'en')
        }

    def testContextMatters(self):
        response = self.translators['en-nl'].translate(TranslationQuery(
            before_context='Dark',
            query='matter',
            after_context='is to be found in the universe'))

        self.assertEqual(response.get_raw_translations()[0], 'materie')

    def testWithoutContext(self):
        response = self.translators['nl-en'].translate(TranslationQuery(
            query='boom'
        ))

        self.assertEquals(response.get_raw_translations()[0], 'tree')

    def testSuffixIsEmpty(self):
        response = self.translators['es-en'].translate(TranslationQuery(
            before_context='Estoy en la',
            query='cama',
            after_context=''))

        self.assertEqual(response.get_raw_translations()[0], 'bed')

    def testUnicodeCharactersInContext(self):
        response = self.translators['de-en'].translate(TranslationQuery(
            before_context='Ein',
            query='klein',
            after_context=u'löwe'))

        self.assertEqual(response.get_raw_translations()[0], "small")

    def testUnicodeCharactersInWordToTranslate(self):
        response = self.translators['de-en'].translate(TranslationQuery(
            before_context=u'Die schön',
            query=u'löwen',
            after_context=u' geht zum Wald'))

        self.assertIn(response.get_raw_translations()[0], ['lion', 'beautiful lion'])

    def testUnicodeInResult(self):
        response = self.translators['en-de'].translate(TranslationQuery(
            before_context='The ',
            query='lion',
            after_context=' goes to the forrest.'))

        self.assertEqual(response.get_raw_translations()[0], u'Löwe')

    def testSuffixStartsWithPunctuation(self):
        response = self.translators['es-en'].translate(TranslationQuery(
            before_context='Estoy en la',
            query='cama',
            after_context=', e soy dormiendo'))

        self.assertEqual(response.get_raw_translations()[0], 'bed')

        response = self.translators['es-en'].translate(TranslationQuery(
            before_context='Estoy en la',
            query='cama',
            after_context=' , e soy dormiendo'))

        self.assertEqual(response.get_raw_translations()[0], 'bed')

    def testQueryEndsWithPunctuation(self):
        translation = self.translators['es-en'].translate(TranslationQuery(
            before_context='Estoy en la',
            query='cama,',
            after_context=' e soy dormiendo'))

        self.assertIn(translation.get_raw_translations()[0], ['bed,', 'bed'])

    def test_strange_span_in_return(self):
        response = self.translators['de-en'].translate(TranslationQuery(
            before_context='Ich hatte mich',
            query='eigentlich schon',
            after_context=' mit dem 1:1-Unentschieden abgefunden'))

        self.assertNotIn("</span>", response.get_raw_translations()[0])

    def test_escaped_characters_in_translation(self):
        response = self.translators['de-en'].translate(TranslationQuery(
            before_context=u'Um Fernbusse aus dem Geschäft zu drängen, hat das Unternehmen damit begonnen, das',
            query='konzerneigene Flaggschiff',
            after_context=u'ICE straßentauglich zu machen. '))

        self.assertNotIn('&#39;', response.get_raw_translations()[0])

    def test_encoding_issue(self):
        response = self.translators['nl-en'].translate(TranslationQuery(
            before_context='De verkiezingscommissie bestaat uit vertegenwoordigers uit verschillende geledingen van '
                           'de universiteit en moet over de goede gang van zaken waken voor en tijdens de',
            query='rectorverkiezing',
            after_context='. De Leuvense studenten hebben deze ochtend laten weten er niet meer aan deel te willen '
                          'nemen. Dat meldt het studentenblad Veto en wordt bevestigd aan onze redactie.'
        ))

        self.assertIn(response.get_raw_translations()[0], ['rector\'s election', 'presidential election'])

    def test_html_in_query(self):
        response = self.translators['nl-en'].translate(TranslationQuery(
               query='m\'n maat'
        ))

        self.assertEqual(response.get_raw_translations()[0], 'My partner')
