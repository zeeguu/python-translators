from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

from wordnik import swagger, WordApi

import nltk

API_URL = 'http://api.wordnik.com/v4'
MAX_WORDS_IN_DEFINITION = 42
quote_characters = ["'", '"']

META_DEFINITION_PREFIXES = [
    "Present participle of",
    "Simple past tense and past participle of",
    "Plural form of",
    "Past participle of",
    "Simple past tense and past participle of",
    "The property of being able to"  # found once with recoverability
]


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

    def _get_pos_tag(self, query):
        full_sentence = nltk.word_tokenize(query.before_context + " " + query.query + query.after_context)
        pos_tags = nltk.pos_tag(full_sentence)

        for each in pos_tags:
            if each[0] == query.query:
                if each[1].startswith("V"):
                    return "verb"
                elif each[1].startswith("N"):
                    return "noun"

        return ""

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query: 
        :return: 
        """

        pos = self._get_pos_tag(query)
        response = self.word_api.getDefinitions(query.query, partOfSpeech=pos)
        if not response:

            if self._query_is_uppercase(query):
                query.query = query.query.lower()
                return self._translate(query)

            elif self._query_starts_with_quote(query):
                # try to see whether the problem is due to 'quotes' around the word name
                self._remove_quotes(query)
                return self._translate(query)

        if not response:
            response = []

        translations = []
        quality = int(self.get_quality())

        for d in response[:query.max_translations]:
            quality -= 1

            definition = self.definition_without_example_and_without_see_synonims(d)
            if self.not_too_long(definition):
                translations.append(self.make_translation(definition, quality))

            meta_defined_word = self.is_meta_definition(definition)
            if meta_defined_word:
                response2 = self.word_api.getDefinitions(meta_defined_word)
                for d2 in response2[:query.max_translations]:
                    d2clean = self.definition_without_example_and_without_see_synonims(d2)
                    if self.not_too_long(d2clean):
                        translations.append(self.make_translation(meta_defined_word + ": " + d2clean, quality))

        if not translations:
            # if we don't know the translation, just parrot back the question
            translations.append(self.make_translation(query.query, quality))

        rez = TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )

        return rez

    def not_too_long(self, definition):
        return len(definition.split(" ")) < MAX_WORDS_IN_DEFINITION

    def is_meta_definition(self, definition: str):
        for prefix in META_DEFINITION_PREFIXES:
            if prefix in definition:
                return definition.split(prefix)[1].strip(" ,.;")
        return None

    def definition_without_example_and_without_see_synonims(self, definition):

        rez = definition.text.split(":")[0]
        rez = rez.split(".")[0]
        return rez

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0

    def _query_is_uppercase(self, query):
        return query.query[0].isupper()

    def _query_starts_with_quote(self, query):
        return query.query[0] in quote_characters

    def _remove_quotes(self, query):
        for quote in quote_characters:
            if query.query.startswith(quote) and query.query.endswith(quote):
                query.query = query.query[1:-1]
