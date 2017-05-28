# -*- coding: utf8 -*-
import unittest
from unittest import TestCase

from translators.composite.best_effort import BestEffortTranslator
from translators.factories.google_translator_factory import GoogleTranslatorFactory


class TestCompositeTranslator(TestCase):
    def setUp(self):
        self.translator = BestEffortTranslator("nl", "en")

    def testContextMatters(self):
        translations = self.translator.ca_translate(before_context='Dit album heeft ons nog dichter bij',
                                                             query='elkaar',
                                                             after_context='gebracht.',
                                                    max_translations=4)
        print (translations)
        self.assertEqual(4, len(translations))

