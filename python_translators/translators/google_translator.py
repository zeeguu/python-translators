# -*- coding: utf-8 -*-

import re

import html.parser
from googleapiclient.discovery import build
import xml.etree.ElementTree as ET

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag
re_closing_tag = re.compile(r"(.*?)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag

COST_PER_CHARACTER = 2000 / 1_000_000  # 20 euro per 1 million characters


class GoogleTranslator(Translator):

    gt_instance = None

    def __init__(self, source_language: str, target_language: str, key: str) -> None:
        super(GoogleTranslator, self).__init__(source_language, target_language)

        self.key = key
        self.translation_service = build('translate', 'v2', developerKey=key)
        self.time_expenses = []

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        if not query.is_context_aware_request():
            return TranslationResponse(
                translations=[self._simple_translate(query.query)],
                costs=TranslationCosts(
                    money=len(query.query) * COST_PER_CHARACTER
                )
            )

        google_query = f'{query.before_context}<span>{query.query}</span>{query.after_context}'

        costs = TranslationCosts(money=len(google_query) * COST_PER_CHARACTER)

        translation = self._simple_translate(f'{query.before_context}<span>{query.query}</span>{query.after_context}')

        unescaped_translation = html.unescape(translation)

        return TranslationResponse(
            translations=[GoogleTranslator.parse_spanned_string(unescaped_translation)],
            costs=costs
        )

    def _simple_translate(self, text: str) -> str:
        params = {
            'source': self.source_language,
            'target': self.target_language,
            'q': f'{text}'
        }

        translation = self.translation_service.translations().list(**params).execute()

        # parse
        return translation['translations'][0]['translatedText']

    @staticmethod
    def parse_spanned_string(spanned_string: str) -> str:

        xml_object = ET.fromstring('<s>' + spanned_string + '</s>')

        found_span = xml_object.find('span')

        if found_span is None:
            return spanned_string

        return found_span.text
