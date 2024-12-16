import json
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
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient


HTML_TAG = "span"

COST_PER_CHARACTER = 1000 / 1_000_000  # 10 euro per 1 million characters

from python_translators.utils import format_dict_for_logging, current_milli_time
from python_translators import logger
from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.response_processors.unescape_html import UnescapeHtml


class MicrosoftTranslator(Translator):
    gt_instance = None
    token = None

    def __init__(
        self,
        source_language: str,
        target_language: str,
        key: str,
        translator_name: str = "Microsoft",
        quality: int = 50,
        service_name: str = "Microsoft",
    ) -> None:
        super(MicrosoftTranslator, self).__init__(
            source_language=source_language,
            target_language=target_language,
            quality=quality,
            service_name=service_name,
            translator_name=translator_name,
        )

        self.key = key

        credential = AzureKeyCredential(self.key)
        self.text_translator = TextTranslationClient(credential=credential)

        self.add_query_processor(EscapeHtml())
        self.add_response_processor(UnescapeHtml())

    @staticmethod
    def _build_raw_query(query: TranslationQuery) -> str:
        return f"{query.before_context}<{HTML_TAG}>{query.query}</{HTML_TAG}>{query.after_context}"

    def _translate(self, query: TranslationQuery) -> TranslationResponse:

        api_query = MicrosoftTranslator._build_raw_query(query)

        response_json = self.text_translator.translate(
            body=[api_query],
            to_language=[self.target_language],
            from_language=self.source_language,
        )

        translation = (
            response_json[0]["translations"][0]["text"] if response_json else None
        )

        # Enclose in <s> tag to make it valid XML (<s> is arbitrarily chosen)
        xml_object = ET.fromstring(f"<s>{translation}</s>")

        parsed_translation = xml_object.find(HTML_TAG).text
        parsed_translation = parsed_translation.strip()

        return TranslationResponse(
            translations=[self.make_translation(parsed_translation)],
            costs=TranslationCosts(money=0),
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return len(MicrosoftTranslator._build_raw_query(query)) * COST_PER_CHARACTER
