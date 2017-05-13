from translators.google_translator import GoogleTranslator
from config_parsing import get_key_from_config
from translators.context_processors.remove_unnecessary_sentences import RemoveUnnecessarySentences
from translators.context_processors.remove_unnecessary_conjunctions import RemoveUnnecessaryConjunctions

conjunctions = {
    'nl': {'en', 'of'},
    'en': {'and', 'or', 'but'},
    'de': {'und', 'oder'}
}


class GoogleTranslatorFactory(object):

    @staticmethod
    def build(source_language, target_language, key=None):
        """
        Builds a Google translator with suitable context processors for the given source and target languages.

        :param source_language: 
        :param target_language: 
        :param key: 
        :return: 
        """

        translator = GoogleTranslatorFactory.build_clean(source_language, target_language, key)

        # Right now only apply the processor to Dutch, English, German and French
        if source_language in ['nl', 'en', 'de', 'fr', 'es']:
            translator.add_context_processor(RemoveUnnecessarySentences(source_language))

        if source_language in conjunctions.keys():
            translator.add_context_processor(RemoveUnnecessaryConjunctions(conjunctions[source_language]))

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

        return GoogleTranslator(source_language, target_language, key)