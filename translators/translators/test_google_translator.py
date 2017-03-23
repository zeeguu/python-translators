from unittest import TestCase
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):

    def setUp(self):
        self.translator = GoogleTranslator ()

    def testContextMatters(self):

        translation1 = self.translator.ca_translate('De directeur', 'treedt', 'af', 'nl', 'en')
        translation2 = self.translator.ca_translate('Dark', 'matter', 'is to be found in the universe', 'en', 'nl')

        assert translation1 == "resigns"
        assert translation2 == "materie"

    def testSuffixIsEmpty(self):

        translation = self.translator.ca_translate('Estoy en la', 'cama', '', 'es', 'en')
        assert translation == "bed"

    def testSuffixStartsWithPunctuation(self):

        translation = self.translator.ca_translate('Estoy en la', 'cama', ', e soy dormiendo', 'es', 'en')
        assert translation == "bed"