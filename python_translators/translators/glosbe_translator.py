from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

import urllib.request, urllib.parse, urllib.error
import requests


class GlosbeTranslator(Translator):

    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def __init__(self, source_language: str, target_language: str) -> None:
        super(GlosbeTranslator, self).__init__(source_language, target_language)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query: 
        :return: 
        """

        # Construct url
        api_url = GlosbeTranslator.build_url(query.query, self.source_language, self.target_language)

        # Send request
        response = requests.get(api_url).json()['tuc']

        # Extract the translations (thanks @SAMSUNG)
        try:
            translations = [translation['phrase']['text'] for translation in response[:query.max_translations]]
        except KeyError:
            translations = []

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        return TranslationCosts(
            money=0
        )

    @staticmethod
    def build_url(query: str, source_language: str, target_language: str) -> str:
        query_params = {
            'from': source_language,
            'dest': target_language,
            'format': 'json',
            'phrase': query.encode('utf-8')
        }

        url = GlosbeTranslator.API_BASE_URL + urllib.parse.urlencode(query_params)
        return url
