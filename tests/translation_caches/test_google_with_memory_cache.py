from unittest import TestCase
from python_translators.translation_caches.memory_cache import MemoryCache
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery


class TestGoogleWithMemoryCache(TestCase):
    def test_something(self):
        translator = GoogleTranslatorFactory.build_with_context(source_language='nl', target_language='en')
        translator.set_cache(MemoryCache(translator_type='google'))

        response = translator.translate(TranslationQuery(
            before_context='De directeur',
            query='treedt af',
            after_context=''
        ))

        # Make the same request
        response2 = translator.translate(TranslationQuery(
            before_context='De directeur',
            query='treedt af',
            after_context=''
        ))