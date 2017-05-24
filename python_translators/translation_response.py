from python_translators.translation_costs import TranslationCosts


class TranslationResponse(object):
    def __init__(self, translations: [str], costs: TranslationCosts):
        self.translations = translations
        self.costs = costs
