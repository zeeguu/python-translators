from unittest import TestCase
from translators import GlosbeTranslator


class TestGoogleTranslator(TestCase):

    def setUp(self):
        self.translator = GlosbeTranslator()

    def testContextMatters(self):

        translations = self.translator.translate("cama", "es", "en", 5)
        assert translations[0] == "bed"
        assert len(translations) == 5