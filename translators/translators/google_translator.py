import os
import urllib

import requests
import re

from configobj import ConfigObj

from context_aware_translator import ContextAwareTranslator

CONFIG_FILE_PATH = '~/.config/translators.cfg'

class GoogleTranslator(ContextAwareTranslator):
    API_BASE_URL = 'https://translation.googleapis.com/language/translate/v2?'

    OPENING_TAG = '<span>'
    CLOSING_TAG = '</ span>'

    def __init__(self, key = None):

        if not key:
            try:
                config_file = os.path.expanduser(CONFIG_FILE_PATH)
                config = ConfigObj(config_file)
                key = config['TRANSLATE_API_KEY']
            except KeyError as e:
                raise Exception ("No config file found. "
                                 "Create config file or pass key as argument to constructor")

        self.key = key

    # Translate a query from source language to target language
    # This translation is not aware of context
    def translate(self, query, source_language, target_language):

        # Construct URL to send request to
        api_url = self.build_url(query, source_language, target_language)

        # Send request
        response = requests.get(api_url)

        if response.status_code == 400:
            error_message = response.json()['error']['message']

            raise Exception(error_message)

        elif response.status_code == 200:
            try:
                return response.json()['data']['translations'][0]['translatedText']

            except KeyError:
                raise Exception('Something went wrong, couldn\'t translate query')

    # Function to translate a query by taking into account the context
    def ca_translate(self, left_context, query, right_context, source_language, target_language):
        query = left_context + '<span>' + query + '</span>' + right_context

        translation = self.translate(query, source_language, target_language)
        translated_query = self.parse_spanned_string(translation)

        return translated_query

    def parse_spanned_string(self, spanned_string):
        re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag

        search_obj = re_opening_tag.search(spanned_string)
        if not search_obj:
            raise Exception('Failed to parse spanned string: no opening span tag found.')

        trail = search_obj.group(1)

        re_closing_tag = re.compile(r"(.*)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag

        search_obj = re_closing_tag.search(trail)

        if not search_obj:
            raise Exception('Failed to parse spanned string: no closing tag found.')

        result = search_obj.group(1)

        return result.strip()

    # Builds up the API URL from the key, query, source language and target language
    def build_url(self, query, source_language, target_language):
        query_params = {
            'key': self.key,
            'target': target_language,
            'source': source_language,
            'q': query,
            'format': 'html'
        }

        encoded_query_params = urllib.urlencode(query_params)

        return GoogleTranslator.API_BASE_URL + encoded_query_params
