from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import merge_translations


class CompositeTranslator(Translator):
    def __init__(self, source_language: str, target_language: str, translators: [Translator] = None) -> None:
        super(CompositeTranslator, self).__init__(source_language, target_language)

        if not translators:
            self.translators: [Translator] = []
        else:
            self.translators: [Translator] = translators

            # Make sure the source and target languages match the source and target languages
            # of the CompositeTranslator
            for t in translators:
                assert t.source_language == source_language
                assert t.target_language == target_language

    def add_translator(self, translator: Translator):
        assert translator.source_language == self.source_language
        assert translator.target_language == self.target_language

        self.translators.append(translator)

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        pass

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        translations = []
        money_costs = 0

        for t in self.translators:
            response = t.translate(query)
            translations = merge_translations(translations, response.translations)
            money_costs += response.costs.money

        return TranslationResponse(translations, costs=TranslationCosts(money=money_costs))
