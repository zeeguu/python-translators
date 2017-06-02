from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

import urllib.request
import urllib.parse
import urllib.error
import requests
import xml.etree.ElementTree as ET

from python_translators.utils import code_to_full_language, get_key_from_config

SUPPORTED_TRANSLATIONS = {
    'es': ['en'],  # Spanish can only be translated to English
    'fr': ['en'],  # French can only be translated to English
    'it': ['en'],  # Italian can only be translated to English
    'en': ['it', 'fr', 'es'],  # English can be translated to Italian, French and Spanish
}

API_BASE_URL = 'https://api.collinsdictionary.com/api/v1'


class CollinsTranslator(Translator):
    gt_instance = None

    def __init__(self, source_language: str, target_language: str, key=None):
        super(CollinsTranslator, self).__init__(source_language, target_language)

        CollinsTranslator.assert_languages_are_supported(self.source_language, self.target_language)

        if not key:
            key = get_key_from_config('COLLINS_TRANSLATE_API_KEY')

        self.key = key

    @classmethod
    def unique_instance(cls, source_language: str, target_language: str, key: str = None) -> 'CollinsTranslator':
        if CollinsTranslator.gt_instance:
            return CollinsTranslator.gt_instance

        CollinsTranslator.gt_instance = CollinsTranslator(source_language, target_language, key)
        return CollinsTranslator.gt_instance

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        dict_code = self.language_codes_to_dict_code(self.source_language, self.target_language)

        query_params = {
            'q': query.query,
            'format': 'xml'
        }

        api_url = '%(base_url)s/dictionaries/%(dict_code)s/search/first?%(query_params)s' % {
            'base_url': API_BASE_URL,
            'dict_code': dict_code,
            'query_params': urllib.parse.urlencode(query_params)
        }

        # Decode JSON response
        json_response = requests.get(api_url, headers=self._get_base_headers()).json()

        # Make sure key is valid
        if 'errorCode' in json_response:
            raise Exception(json_response['errorMessage'])

        # Construct XML object
        xml_tree = ET.ElementTree(ET.fromstring(json_response['entryContent'].encode('utf-8')))

        return TranslationResponse(
            translations=[xml_tree.iter('quote').next().text],
            costs=TranslationCosts(money=0)  # a (limited) free API
        )

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        return TranslationCosts(
            money=0
        )

    def _get_base_headers(self) -> dict:
        return {
            'accessKey': self.key
        }

    @staticmethod
    def language_codes_to_dict_code(code1: str, code2: str) -> str:
        return '%(language1)s-%(language2)s' % {
            'language1': code_to_full_language(code1),
            'language2': code_to_full_language(code2),
        }

    @staticmethod
    def assert_languages_are_supported(source_language: str, target_language: str):
        full_source_language = code_to_full_language(source_language)
        full_target_language = code_to_full_language(target_language)

        if source_language not in SUPPORTED_TRANSLATIONS:
            raise Exception('Can not translate %(full_source_language)s' % locals())

        if target_language not in SUPPORTED_TRANSLATIONS[source_language]:
            raise Exception('Can not translate %(full_source_language)s to %(full_target_language)s' % locals())