from python_translators.translation_costs import TranslationCosts
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translators.glosbe_translator import GlosbeTranslator
from torrequest import TorRequest
from time import sleep
import requests

"""
	similar to GlosbeTranslator
	blocks and resends translation requests when Glosbe refuses to accept request due to too many connections
	in this case manual intervention is required by translating a word through Glosbe's web page and answering the captcha
"""


class GlosbePendingTranslator(GlosbeTranslator):

    def __init__(self, source_language: str, target_language: str, translator_name: str = 'Glosbe', quality: int = '50',
                 service_name: str = 'Glosbe') -> None:
        super(GlosbePendingTranslator, self).__init__(source_language, target_language, translator_name, quality, service_name)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query:
        :return:
        """

        # Construct url
        api_url = GlosbeTranslator.build_url(query.query, self.source_language, self.target_language)

        # Send request
        response = requests.get(api_url).json()
        
        # Attempt request each 5 seconds
        while response['result'] == 'error':
            print('awaiting reset')
            sleep(5)
            #print('new_connection: ', self.tr.get('http://ipecho.net/plain').text)
            response = requests.get(api_url).json()
        
        response = response['tuc']
        
        # Extract the translations
        translations = []
        try:
            for translation in response[:query.max_translations]:
                translations.append(self.make_translation(translation['phrase']['text']))

        except KeyError:
            pass

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )
