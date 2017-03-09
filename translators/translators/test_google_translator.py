import os
from unittest import TestCase
from configobj import ConfigObj
from translators import GoogleTranslator


class TestGoogleTranslator(TestCase):

    def testSimple(self):
        config_file = os.path.expanduser('~/.zeeguu/zeeguu_api.cfg')

        config = ConfigObj(config_file)
        translator = GoogleTranslator (config['TRANSLATE_API_KEY'])

        translation = translator.ca_translate('De directeur', 'treedt', 'af', 'nl', 'en')
        print translation #== u"resigns"

        translation = translator.ca_translate('Dark', 'matter', 'is to be found in the universe', 'en', 'nl')
        print translation

