# -*- coding: utf-8 -*-

import re

# note that this used to be apiclient, but in the newest versions is googleapiclient
# https://stackoverflow.com/questions/18267749/importerror-no-module-named-apiclient-discovery#23521799
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import xml.etree.ElementTree as ET

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.response_processors.unescape_html import UnescapeHtml

re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag
re_closing_tag = re.compile(r"(.*?)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag

COST_PER_CHARACTER = 2000 / 1_000_000  # 20 euro per 1 million characters
HTML_TAG = 'span'


class GoogleTranslator(Translator):
    def __init__(self, source_language: str, target_language: str, key: str, translator_name: str = 'Google',
                 quality: int = 50, service_name: str = 'Google') -> None:

        super(GoogleTranslator, self).__init__(
            source_language=source_language,
            target_language=target_language,
            service_name=service_name,
            translator_name=translator_name,
            quality=quality
        )

        self.key = key
        try:
            self.translation_service = build('translate', 'v2', developerKey='bla')
        except HttpError as e:
            raise Exception(e.resp.status)

        self.add_query_processor(EscapeHtml())
        self.add_response_processor(UnescapeHtml())

    @staticmethod
    def _cost_of_query(query: str):
        return len(query) * COST_PER_CHARACTER

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        if not query.is_context_aware_request():
            return TranslationResponse(
                costs=TranslationCosts(money=GoogleTranslator._cost_of_query(query.query)),
                translations=[self.make_translation(translation=self._simple_translate(query.query))]
            )

        google_query = f'{query.before_context}<{HTML_TAG}>{query.query}</{HTML_TAG}>{query.after_context}'

        costs = TranslationCosts(money=GoogleTranslator._cost_of_query(query.query))

        translation = self._simple_translate(google_query)

        translation_response = TranslationResponse(costs=costs)

        try:
            result = GoogleTranslator.parse_spanned_string(translation)
            translation_response.add_translation(self.make_translation(result))

        except ValueError:
            pass

        return translation_response

    def compute_money_costs(self, query: TranslationQuery) -> float:
        money = len(query.query) * COST_PER_CHARACTER

        if query.is_context_aware_request():
            money += (len(f'<{HTML_TAG}>') + len(f'</{HTML_TAG}>')) * COST_PER_CHARACTER

        return money

    def _simple_translate(self, text: str) -> str:
        params = {
            'source': self.source_language,
            'target': self.target_language,
            'q': text
        }

        translation = self.translation_service.translations().list(**params).execute()

        return translation['translations'][0]['translatedText']

    @staticmethod
    def parse_spanned_string(spanned_string: str) -> str:

        xml_object = ET.fromstring('<s>' + spanned_string + '</s>')

        found_span = xml_object.find('span')

        if found_span is None:
            raise ValueError('No span tag found in input!')

        return found_span.text
