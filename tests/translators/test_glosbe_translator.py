import unittest
from unittest import TestCase
from translators import GlosbeTranslator


class TestGlosbeTranslator(TestCase):

    def setUp(self):
        self.translator = GlosbeTranslator()

    def testNumberOfTranslationsWorks(self):

        translations = self.translator.translate("cama", "es", "en", 5)
        assert translations[0] == "bed"
        assert len(translations) == 5

        translations = self.translator.translate("cama", "es", "en", 3)
        assert translations[0] == "bed"
        assert len(translations) == 3


if __name__ == '__main__':
    unittest.main()
