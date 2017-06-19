from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translation_costs import TranslationCosts
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.query_processors.remove_all_context import RemoveAllContext
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory
from python_translators.translators.glosbe_translator import GlosbeTranslator


class BestEffortTranslator(Translator):

    def __init__(self, source_language: str, target_language: str) -> None:
        super(BestEffortTranslator, self).__init__(source_language, target_language)

        self.translators = []

        # Add a regular google translator
        self.translators.append(GoogleTranslatorFactory.build(source_language, target_language))

        # Add a google translator that ignores context
        t = GoogleTranslatorFactory.build(source_language, target_language)
        t.add_query_processor(RemoveAllContext())
        self.translators.append(t)

        # Add a microsoft translator
        self.translators.append(MicrosoftTranslatorFactory.build(source_language, target_language))

        # Add a microsoft translator that ignores context
        t = MicrosoftTranslatorFactory.build(source_language, target_language)
        t.add_query_processor(RemoveAllContext())
        self.translators.append(t)

        # Add a Glosbe translator
        self.translators.append(GlosbeTranslator(source_language, target_language))

    def _estimate_costs(self, query: TranslationQuery) -> TranslationCosts:
        return TranslationCosts(
            money=10
        )

    def _translate(self, query: TranslationQuery) -> TranslationResponse:

        translations = []
        costs = TranslationCosts(money=0)  # no costs yet

        max_translations = query.max_translations

        for translator in self.translators:

            # Reached the max number of translations?
            if len(translations) >= max_translations:
                break

            query.max_translations = max_translations - len(translations)

            # Perform translation
            response = translator.translate(query)

            assert len(response.translations) <= query.max_translations

            # Add translations
            for translation in response.translations:

                if translation.lower() not in map(lambda s: s.lower(), translations):
                    translations.append(translation)

            # Add costs
            costs.money += response.costs.money

        return TranslationResponse(
            translations=translations,
            costs=costs
        )


if __name__ == '__main__':
    t = BestEffortTranslator(source_language='nl', target_language='en')
    r = t.translate(TranslationQuery(
        before_context='De directeur',
        query='treedt af',
        after_context='',
    ))

    print(vars(r))