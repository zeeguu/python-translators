from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts

import requests


class ReverseTranslator(Translator):

    def __init__(self, source_language: str, target_language: str, translator_name: str = 'Reverse',
                 quality: int = '10',
                 service_name: str = 'Reverse') -> None:
        super(ReverseTranslator, self).__init__(source_language, target_language, translator_name, quality,
                                                service_name)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query: 
        :return: 
        """

        simple_reverse = self.make_translation(query.query[::-1])
        title_reverse = self.make_translation(query.query[::-1].title())
        upper_reverse = self.make_translation(query.query[::-1].upper())
        translations = [simple_reverse, title_reverse, upper_reverse][:query.max_translations]

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0
