from python_translators.translators.google_translator import GoogleTranslator
from python_translators.utils import get_key_from_config
from python_translators.query_processors.remove_unnecessary_sentences import RemoveUnnecessarySentences
from python_translators.query_processors.remove_unnecessary_conjunctions import RemoveUnnecessaryConjunctions
from python_translators.query_processors.remove_all_context import RemoveAllContext

from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.response_processors.unescape_html import UnescapeHtml


conjunctions = {
    'nl': {'en', 'of'},
    'en': {'and', 'or', 'but'},
    'de': {'und', 'oder'}
}


class GoogleTranslatorFactory(object):

    @staticmethod
    def build(source_language: str, target_language: str, key=None) -> GoogleTranslator:
        """
        Builds a Google translator with suitable context processors for the given source and target languages.

        :param source_language: 
        :param target_language: 
        :param key: 
        :return:
        """

        translator = GoogleTranslatorFactory.build_clean(source_language, target_language, key)

        # Right now only apply the processor to Dutch, English, German, French, Spanish
        if source_language in ['nl', 'en', 'de', 'fr', 'es']:
            translator.add_query_processor(RemoveUnnecessarySentences(source_language))

        if source_language in list(conjunctions.keys()):
            translator.add_query_processor(RemoveUnnecessaryConjunctions(conjunctions[source_language]))

        translator.add_query_processor(EscapeHtml())
        translator.add_response_processor(UnescapeHtml())

        translator.translator_name = 'Google - with context'

        return translator

    @staticmethod
    def build_contextless(source_language: str, target_language: str, key=None) -> GoogleTranslator:
        """
        Builds a Google translator that ignores all context.

        :param source_language:
        :param target_language:
        :param key:
        :return:
        """
        translator = GoogleTranslatorFactory.build_clean(source_language, target_language, key)

        translator.add_query_processor(RemoveAllContext())
        translator.add_query_processor(EscapeHtml())
        translator.add_response_processor(UnescapeHtml())

        translator.translator_name = 'Google - without context'

        return translator

    @staticmethod
    def build_clean(source_language, target_language, key=None):
        """
        Builds a clean Google translator. This means that it has no context processors attached.
        
        :param source_language: 
        :param target_language:
        :param key: 
        :return: 
        """
        if key is None:
            key = get_key_from_config('GOOGLE_TRANSLATE_API_KEY')

        return GoogleTranslator(source_language=source_language,
                                target_language=target_language,
                                key=key,
                                service_name='Google',
                                translator_name='Google'
                                )
