from translator import Translator
import urllib
import requests


class GlosbeTranslator(Translator):

    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def translate(self, query, source_language, target_language, max_translations=1):

        # Construct url
        api_url = GlosbeTranslator.build_url(query, source_language, target_language)

        # Send request
        response = requests.get(api_url)

        # Extract translation
        try:
            return response.json()['tuc'][0]['phrase']['text']
        except Exception:
            raise Exception('Something went wrong, could\'t translate query')

    @staticmethod
    def build_url(query, source_language, target_language):
        query_params = {
            'from': source_language,
            'dest': target_language,
            'format': 'json',
            'phrase': query
        }

        return GlosbeTranslators.API_BASE_URL + urllib.urlencode(query_params)
