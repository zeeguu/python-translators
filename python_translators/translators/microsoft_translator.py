import urllib.request
import urllib.parse
import urllib.error
import requests
import time
import xml.etree.ElementTree as ET

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

TOKEN_SERVICE_URL = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
TRANSLATION_SERVICE_URL = 'https://api.microsofttranslator.com/V2/Http.svc/Translate'

HTML_TAG = 'span'

COST_PER_CHARACTER = 1000 / 1_000_000  # 10 euro per 1 million characters

from python_translators.utils import format_dict_for_logging, current_milli_time
from python_translators import logger
from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.response_processors.unescape_html import UnescapeHtml


class MicrosoftTranslator(Translator):
    gt_instance = None
    token = None

    def __init__(self, source_language: str, target_language: str, key: str, translator_name: str = 'Microsoft',
                 quality: int = 50, service_name: str = 'Microsoft') -> None:
        super(MicrosoftTranslator, self).__init__(
            source_language=source_language,
            target_language=target_language,
            quality=quality,
            service_name=service_name,
            translator_name=translator_name,
        )

        self.key = key
        self.refresh_token_if_needed()

        self.add_query_processor(EscapeHtml())
        self.add_response_processor(UnescapeHtml())

    @staticmethod
    def _build_raw_query(query: TranslationQuery) -> str:
        return f'{query.before_context}<{HTML_TAG}>{query.query}</{HTML_TAG}>{query.after_context}'

    def _translate(self, query: TranslationQuery) -> TranslationResponse:

        api_query = MicrosoftTranslator._build_raw_query(query)

        translation = self.send_translation_request(api_query, 'text/html')

        # Enclose in <s> tag to make it valid XML (<s> is arbitrarily chosen)
        xml_object = ET.fromstring(f'<s>{translation}</s>')

        parsed_translation = xml_object.find(HTML_TAG).text

        return TranslationResponse(
            translations=[self.make_translation(parsed_translation)],
            costs=TranslationCosts(
                money=0
            )
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return len(MicrosoftTranslator._build_raw_query(query)) * COST_PER_CHARACTER

    def send_translation_request(self, query: str, content_type: str) -> str:
        """
        Sends a translation request to the Microsoft Translation service, query parameters are

        :param query:
        :param content_type:
        :return:
        """

        self.refresh_token_if_needed()

        # Build query parameters
        query_params = {
            'text': query.encode('utf-8'),
            'from': self.source_language,
            'to': self.target_language,
            'contentType': content_type,
        }

        # Build headers
        headers = {
            'Accept': 'application/xml',
            'Authorization': 'Bearer ' + self.token['token'],
        }

        # Send request to API
        encoded_params = urllib.parse.urlencode(query_params)

        response = requests.get(f'{TRANSLATION_SERVICE_URL}?{encoded_params}', headers=headers)

        xml_object = ET.fromstring(response.text.encode('utf-8'))

        return xml_object.text

    def refresh_token_if_needed(self) -> None:
        if MicrosoftTranslator.token_is_invalid():
            MicrosoftTranslator.token = MicrosoftTranslator.request_token(self.key)

    @staticmethod
    def request_token(key) -> dict:
        logger.info(format_dict_for_logging(dict(EVENT='MICROSOFT_REQUEST_TOKEN')))
        t1 = current_milli_time()

        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Accept": 'application/jwt',
            'Content-Type': 'application/json',
        }

        response = requests.post('https://api.cognitive.microsoft.com/sts/v1.0/issueToken', headers=headers)

        time_passed = current_milli_time() - t1

        logger.info(format_dict_for_logging(dict(EVENT='MICROSOFT_RECEIVED_TOKEN', TIME_PASSED=time_passed)))
        if response.status_code == 401:
            raise Exception('Access denied due to invalid subscription key. Make sure to provide a valid key for an '
                            'active subscription.')

        if response.status_code != 200:
            raise Exception('Something went wrong when requesting a new token.')

        return {
            'expiresAt': time.time() + (60 * 8),  # expire after 8 minutes
            'token': response.text,
        }

    @staticmethod
    def token_is_invalid():
        return MicrosoftTranslator.token is None or time.time() >= MicrosoftTranslator.token['expiresAt']
