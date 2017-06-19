from python_translators.translation_costs import TranslationCosts
from python_translators.utils import merge_unique


class TranslationResponse(object):
    def __init__(self, translations: [dict]=None, costs: TranslationCosts = None):
        self.translations = translations if translations else []
        self.costs = costs if costs else TranslationCosts()

    def add_translation(self, translation) -> None:
        self.translations.append(translation)

    def get_raw_translations(self):
        """
        Returns a list of translations where each translation is a string.
        :return:
        """
        return [t['translation'] for t in self.translations]


def merge_translations(translations1: [], translations2: [[]]):
    return merge_unique(translations1, translations2, lambda x, y: x.lower() == y.lower())
