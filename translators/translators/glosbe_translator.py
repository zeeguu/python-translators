from .translator import Translator
import urllib.request, urllib.parse, urllib.error
import requests


class GlosbeTranslator(Translator):

    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def __init__(self, source_language, target_language):
        super(GlosbeTranslator, self).__init__(source_language, target_language)

    def translate(self, query, max_translations=2):

        """

            Returns a list of max_translations possible translations for the given word.
            
        :param query: 
        :param source_language: 
        :param target_language: 
        :param max_translations: 
        
        :return: a list of possible translations 
        """

        # Construct url
        api_url = GlosbeTranslator.build_url(query, self.source_language, self.target_language)

        # Send request
        response = requests.get(api_url).json()['tuc']

        # Extract the translations (thanks @SAMSUNG)
        translations = [translation['phrase']['text'] for translation in response[:max_translations]]

        return translations

    @staticmethod
    def build_url(query, source_language, target_language):
        query_params = {
            'from': source_language,
            'dest': target_language,
            'format': 'json',
            'phrase': query.encode('utf-8')
        }

        url = GlosbeTranslator.API_BASE_URL + urllib.parse.urlencode(query_params)
        return url
