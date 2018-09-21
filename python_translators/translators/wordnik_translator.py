from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

from wordnik import swagger, WordApi

API_URL = 'http://api.wordnik.com/v4'
MAX_WORDS_IN_DEFINITION = 16


class WordnikTranslator(Translator):
    """

        more like a dictionary than a translator.
        translates from english to english

    """

    def __init__(self, source_language: str, target_language: str, key: str, translator_name: str = 'Wordnik',
                 quality: int = '70',
                 service_name: str = 'Wordnik') -> None:
        super(WordnikTranslator, self).__init__(
            source_language, target_language, translator_name, quality,
            service_name)

        self.key = key

        self.api_client = swagger.ApiClient(self.key, API_URL)
        self.word_api = WordApi.WordApi(self.api_client)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query: 
        :return: 
        """

        if self.source_language != "en" and self.target_language != "en":
            return []

        response = self.word_api.getDefinitions(query.query)

        # Extract the translations (thanks @SAMSUNG)
        translations = []
        quality = int(self.get_quality())

        for definition in response[0:query.max_translations]:
            try:
                quality -= 1
                if len(definition.text.split(" ")) < MAX_WORDS_IN_DEFINITION:
                    translations.append(self.make_translation(definition.text, str(quality)))
            except KeyError:
                pass

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0
