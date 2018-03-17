from python_translators.translators.translator import Translator

from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts


class DuplicateTranslator(Translator):

    """

        a dummy translator useful for the tests
        does nothing else than duplicates the original query.

    """


    def __init__(self, source_language: str, target_language: str, translator_name: str = 'Reverse',
                 quality: int = '10',
                 service_name: str = 'Reverse') -> None:
        super(DuplicateTranslator, self).__init__(source_language, target_language, translator_name, quality,
                                                service_name)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query: 
        :return: 
        """

        duplicate = self.make_translation(query.query+query.query)
        translations = [duplicate]

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # no costs for this
            )
        )

    def compute_money_costs(self, query: TranslationQuery) -> float:
        return .0
