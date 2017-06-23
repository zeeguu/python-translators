from unittest import TestCase
from python_translators.translation_caches.memory_cache import MemoryCache
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import make_translation


class TestMemoryCache(TestCase):
    def setUp(self):
        self.cache = MemoryCache('type')

    def test_empty_cache(self):
        result = self.cache.fetch(TranslationQuery(
            before_context='De directeur',
            query='treedt af',
            after_context=''
        ), source_language='nl', target_language='en')

        self.assertEqual(result, [])

    def test_filled_cache(self):

        # Build a query
        query = TranslationQuery(
            before_context='De directeur',
            query='treedt af',
            after_context=''
        )

        # Some made up results
        translations = [
            make_translation('resigns', 60, 'Google'),
            make_translation('ends', 40, 'Google')
        ]

        lang_config = dict(
            source_language='nl',
            target_language='en',
        )

        # Store results in the cache
        self.cache.store(query=query, **lang_config, translations=translations)

        results_from_cache = self.cache.fetch(
            query=query,
            **lang_config
        )

        self.assertEqual(results_from_cache, translations)

    def test_merging_cache_results(self):
        # Build a query
        query = TranslationQuery(
            before_context='De directeur',
            query='treedt af',
            after_context=''
        )

        # Some made up results
        translations = [
            make_translation('resigns', 60, 'Google'),
            make_translation('ends', 40, 'Google')
        ]

        lang_config = dict(
            source_language='nl',
            target_language='en',
        )

        # Store results in the cache
        self.cache.store(query=query, **lang_config, translations=translations)

        more_translations = [
            make_translation('stops', 55, 'Microsoft'),
        ]

        self.cache.store(query=query, **lang_config, translations=[
            make_translation('stops', 55, 'Microsoft')
        ])

        results_from_cache = self.cache.fetch(query=query, **lang_config)

        self.assertEqual(results_from_cache, translations + more_translations)

