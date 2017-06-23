from python_translators.translation_caches.translation_cache import TranslationCache
from python_translators.translation_caches.cachekey import CacheKey
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_response import merge_translations
from collections import defaultdict

import random

MAX_CACHE_SIZE = 1


class MemoryCache(TranslationCache):
    def __init__(self, translator_type):
        super(MemoryCache, self).__init__(translator_type)
        self.translations = defaultdict(list)

    def store(self, query: TranslationQuery, source_language: str, target_language: str, translations: [dict]):
        key = CacheKey(query, source_language, target_language)

        self.translations[key] = merge_translations(self.translations[key], translations)

        if len(self.translations) > MAX_CACHE_SIZE:
            self.translations.pop(random.choice(self.translations.keys()))


    def fetch(self, query: TranslationQuery, source_language: str, target_language: str) -> [dict]:
        key = CacheKey(query, source_language, target_language)

        return self.translations[key]
