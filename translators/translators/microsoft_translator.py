from context_aware_translator import ContextAwareTranslator
import urllib
import requests
import time
import xml.etree.ElementTree as ET

from config_parsing import get_key_from_config

TOKEN_SERVICE_URL = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
TRANSLATION_SERVICE_URL = 'https://api.microsofttranslator.com/V2/Http.svc/Translate'


class MicrosoftTranslator(ContextAwareTranslator):
    gt_instance = None

    def __init__(self, key=None):
        if not key:
            key = get_key_from_config('MICROSOFT_TRANSLATE_API_KEY')

        self.key = key
        self.token = self.request_token()

    @classmethod
    def unique_instance(cls, key=None):
        """
            The creation of a translator object is slow, since it requires
            fetching a token!

            This is a static class instance that caches a connection and 
            reuses it.

        :return: a cached MicrosoftTranslator object
        """
        if MicrosoftTranslator.gt_instance:
            return MicrosoftTranslator.gt_instance

        MicrosoftTranslator.gt_instance = MicrosoftTranslator(key)
        return MicrosoftTranslator.gt_instance

    def ca_translate(self, before_context, query, after_context, from_language, to_language, max_translations=1):
        raise NotImplemented

    def translate(self, query, source_language, target_language, max_translations=1):

        # Refresh token if necessary
        if time.time() <= self.token['expiresAt']:
            self.refresh_token()

        # Build query parameters
        query_params = {
            'text': query,
            'from': source_language,
            'to': target_language,
            'contentType': 'text/plain',
        }

        # Build headers
        headers = {
            'Accept': 'application/xml',
            'Authorization': 'Bearer ' + self.token['token']
        }

        # Send request and fetch response
        response = requests.get(TRANSLATION_SERVICE_URL + '?' + urllib.urlencode(query_params), headers=headers)

        return MicrosoftTranslator.parse_response(response)

    @staticmethod
    def parse_response(response):
        e = ET.fromstring(response.text)

        return e.text

    def refresh_token(self):
        self.token = self.request_token()

    def request_token(self):
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Accept": 'application/jwt',
            'Content-Type': 'application/json'
        }

        response = requests.post('https://api.cognitive.microsoft.com/sts/v1.0/issueToken', headers=headers)

        if response.status_code == 401:
            raise Exception('Access denied due to invalid subscription key. Make sure to provide a valid key for an '
                            'active subscription.')

        if response.status_code != 200:
            raise Exception('Something went wrong when requesting a new token.')

        return {
            'expiresAt': time.time() + (60 * 8),  # expire after 8 minutes
            'token': response.text
        }
