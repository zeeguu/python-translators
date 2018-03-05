# -*- coding: utf8 -*-
from unittest import TestCase

from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory


class TestMicrosoftTranslator(TestCase):
    def setUp(self):
        self.microsoft = MicrosoftTranslatorFactory.build_with_context('en', 'zh-CN')
        self.google = GoogleTranslatorFactory.build_with_context('en', 'zh-CN')

    def test_water_is_water_in_all_translators(self):
        query = TranslationQuery(
            before_context='This',
            query='water',
            after_context='is good')

        mresponse = self.microsoft.translate(query)
        gresponse = self.google.translate(query)

        self.assertTrue(mresponse.get_raw_translations() == gresponse.get_raw_translations())

        # language codes for google from: https://ctrlq.org/code/19899-google-translate-languages
