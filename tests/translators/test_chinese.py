# -*- coding: utf8 -*-
from unittest import TestCase

from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory


class TestMicrosoftTranslator(TestCase):
    def setUp(self):
        self.microsoft = MicrosoftTranslatorFactory.build_with_context('en', 'zh-CN')

        # language codes for google from: https://ctrlq.org/code/19899-google-translate-languages
        self.google = GoogleTranslatorFactory.build_with_context('en', 'zh-CN')

    def test_water_is_water_in_both_google_and_microsoft(self):
        query = TranslationQuery(
            before_context='This',
            query='water',
            after_context='is good')

        m_response = self.microsoft.translate(query)
        g_response = self.google.translate(query)

        self.assertTrue(m_response.get_raw_translations() == g_response.get_raw_translations())

