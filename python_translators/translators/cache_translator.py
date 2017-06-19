# -*- coding: utf-8 -*-

import re

from python_translators.translation_caches.translation_cache import TranslationCache

from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts


class CacheTranslator(Translator):

    def __init__(self, source_language: str, target_language: str, translation_cache: TranslationCache):
        super(CacheTranslator, self).__init__(source_language=source_language, target_language=target_language)
        self.translation_cache = translation_cache

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        return TranslationCosts(
            money=0,
        )

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        pass
