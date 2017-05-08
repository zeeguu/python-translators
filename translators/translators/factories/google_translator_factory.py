from translators.google_translator import GoogleTranslator
from config_parsing import get_key_from_config
from translators.context_processors.reduce_to_one_sentence import ReduceToOneSentence
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
        if source_language in ['nl', 'en', 'de', 'fr']:
            translator.add_context_processor(ReduceToOneSentence())

        if source_language in conjunctions:
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


if __name__ == '__main__':
    g = GoogleTranslatorFactory.build('nl', 'en')

    before_context = 'Justitieminister Koen Geens (CD&V) werkt aan een wetsontwerp dat burgerinfiltranten mogelijk ' \
                     'maakt in de strijd tegen'
    after_context = 'en georganiseerde misdaad. Dat zegt hij woensdag in Knack, nadat Brussels procureur-generaal ' \
                    'Johan Delmulle daar vorig najaar een lans voor had gebroken. Daarnaast werkt Geens ook aan een ' \
                    'regeling ' \
                    'rond spijtoptanten. Een akkoord binnen de meerderheid is er nog niet.'

    print(g.ca_translate(query='terrorisme', before_context=before_context, after_context=after_context))
