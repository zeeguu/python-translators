from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.translation_response import merge_responses
from python_translators.utils import current_milli_time


class CompositeTranslator(Translator):
    def compute_money_costs(self, query: TranslationQuery) -> float:
        return sum(translator.compute_money_costs() for translator in self.translators)

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

    def get_translator_name(self):
        return 'Composite(' + self.translator_list_text() + ')'

    def add_translator(self, translator: Translator):
        assert translator.source_language == self.source_language
        assert translator.target_language == self.target_language

        self.translators.append(translator)

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        responses = []

        for translator in self.translators:
            t1 = current_milli_time()
            responses.append(translator.translate(query))
            t2 = current_milli_time()

            query.budget.subtract_time(t2 - t1)

        responses = map(lambda t: t.translate(query), self.translators)

        return merge_responses(responses)

    def translator_list_text(self):
        return ', '.join(map(lambda t: t.get_translator_name(), self.translators))
