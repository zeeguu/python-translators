from python_translators.translation_caches.translation_cache import TranslationCache
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from utils import merge_translations
from collections import defaultdict


class TranslationKey(object):
    def __init__(self, query: TranslationQuery, source_language, target_language):
        self.query = query
        self.source_language = source_language
        self.target_language = target_language

    def __hash__(self):
        return hash((self.query.before_context,
                     self.query.query,
                     self.query.after_context,
                     self.source_language,
                     self.target_language))

    def __eq__(self, other: 'TranslationKey'):
        return (self.query.before_context,
                self.query.query,
                self.query.after_context,
                self.source_language,
                self.target_language) == (other.query.before_context,
                                          other.query.query,
                                          other.query.after_context,
                                          other.source_language,
                                          other.target_language)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)


class MemoryCache(TranslationCache):
    instance = None

    def __init__(self, translator_type):
        super(MemoryCache, self).__init__(translator_type)
        self.translations = defaultdict(list)

    def store(self, query: TranslationQuery, source_language: str, target_language: str, response: TranslationResponse):
        key = TranslationKey(query, source_language, target_language)

        self.translations[key] = merge_translations(self.translations[key], response.translations)

    def fetch(self, query: TranslationQuery, source_language: str, target_language: str):
        key = TranslationKey(query, source_language, target_language)

        return self.translations[key]
