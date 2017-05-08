from ..google_translator import GoogleTranslator


class GoogleTranslatorsFactory(object):

    @staticmethod
    def build(source_language, target_language):
        """
        Builds a Google translator with suitable context processors for the given source and target languages.
        
        :param source_language: 
        :param target_language: 
        :return: 
        """
        return GoogleTranslator(source_language=source_language, target_language=target_language)

    @staticmethod
    def build_clean(source_language, target_language):
        """
        Builds a clean Google translator. This means that it has no context processors attached.
        
        :param source_language: 
        :param target_language: 
        :return: 
        """
        return GoogleTranslator(source_language=source_language, target_language=target_language)
