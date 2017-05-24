from translators.translator import Translator
import urllib.request, urllib.parse, urllib.error
import requests


class GlosbeTranslator(Translator):
    """
    
    """
    API_BASE_URL = 'https://glosbe.com/gapi/translate?'

    def __init__(self, source_language: str, target_language: str) -> None:
        super(GlosbeTranslator, self).__init__(source_language, target_language)

    def _translate(self, query: str, max_translations: int = 2) -> [str]:
        """
        Returns a list of at most `max_translations` possible translations for the given word.
             
        :param query: 
        :param max_translations: 
        
        :return: a list of possible translations 
        """

        # Construct url
        api_url = GlosbeTranslator._build_url(query, self.source_language, self.target_language)

        # Send request
        response = requests.get(api_url).json()['tuc']

        # Extract the translations (thanks @SAMSUNG)
        translations = [translation['phrase']['text'] for translation in response[:max_translations]]

        return translations

    @staticmethod
    def _build_url(query: str, source_language: str, target_language: str) -> str:
        """
        Builds a URL from the given query, source language and target language
        :param query: 
        :param source_language: 
        :param target_language: 
        :return: 
        """
        query_params = {
            'from': source_language,
            'dest': target_language,
            'format': 'json',
            'phrase': query.encode('utf-8')
        }

        url = GlosbeTranslator.API_BASE_URL + urllib.parse.urlencode(query_params)
        return url
