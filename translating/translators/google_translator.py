import urllib

import requests

from context_aware_translator import ContextAwareTranslator


class GoogleTranslator(ContextAwareTranslator):

    API_BASE_URL = 'https://translation.googleapis.com/language/translate/v2?'

    OPENING_TAG = '<span>'
    CLOSING_TAG = '</ span>'

    def __init__(self, key):
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
        query = left_context + GoogleTranslator.OPENING_TAG + query + GoogleTranslator.CLOSING_TAG + right_context

        translated_text = self.translate(query, source_language, target_language)

        index_opening_tag = translated_text.find(GoogleTranslator.OPENING_TAG)
        index_closing_tag = translated_text.find(GoogleTranslator.CLOSING_TAG, index_opening_tag)

        if index_closing_tag == -1:
            index_closing_tag = translated_text.find(GoogleTranslator)

        # Somehow the <p> and/or the </p> tags were lost in translation
        if index_opening_tag == -1 or index_closing_tag == -1:
            raise Exception('Something went wrong, couldn\'t translate query')

        begin = index_opening_tag + len(GoogleTranslator.OPENING_TAG)
        end = index_closing_tag

        # todo: decode encoded symbols

        return translated_text[begin:end]

    # Builds up the API URL from the key, query, source language and target language
    def build_url(self, query, source_language, target_language):
        query_params = {
            'key': self.key,
            'target': target_language,
            'source': source_language,
            'q': query,
            'format': 'text'
        }

        encoded_query_params = urllib.urlencode(query_params)

        return GoogleTranslator.API_BASE_URL + encoded_query_params


