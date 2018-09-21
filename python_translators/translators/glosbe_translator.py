from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

import urllib.request, urllib.parse, urllib.error
import requests

problematic_definition_signs = ["plural form of", "past tense", "past participle", "present participle", "<i>",
                                "&quot;", "present indicative"]


class GlosbeTranslator(Translator):
    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def __init__(self, source_language: str, target_language: str, translator_name: str = 'Glosbe', quality: int = '50',
                 service_name: str = 'Glosbe') -> None:
        super(GlosbeTranslator, self).__init__(source_language, target_language, translator_name, quality, service_name)

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
        translations = []

        for translation in response[1:query.max_translations]:
            try:
                translations.append(self.make_translation(translation['phrase']['text']))
            except KeyError:
                pass

        translation_count = len(translations)
        if translation_count < query.max_translations:
            for meaning in response[0]['meanings']:
                try:
                    this_meaning = meaning['text']
                    this_meaning = this_meaning[0:this_meaning.find("; &quot;")]

                    problematic = False
                    for sign in problematic_definition_signs:
                        if this_meaning.lower().find(sign) != -1:
                            problematic = True
                            print(f"ignoring problematic translation: {this_meaning}")
                            break

                    if problematic:
                        continue

                    if len(this_meaning.split(" ")) < 10:
                        translations.append(self.make_translation(this_meaning))
                        translation_count += 1
                except KeyError:
                    pass

                if translation_count == query.max_translations:
                    break

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0

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
