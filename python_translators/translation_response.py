from python_translators.translation_costs import TranslationCosts
from python_translators.utils import merge_unique


class TranslationResponse(object):
    def __init__(self, translations: [dict]=None, costs: TranslationCosts = None):
        self.translations = translations if translations else []
        self.costs = costs if costs else TranslationCosts()

    def add_translation(self, translation) -> None:
        self.translations.append(translation)

    def get_raw_translations(self) -> [str]:
        """
        Returns a list of translations where each translation is a string.
        :return:
        """
        return [t['translation'] for t in self.translations]

    def get_raw_qualities(self) -> [int]:
        return [t['quality'] for t in self.translations]

    def get_raw_service_names(self) -> [str]:
        return [t['service_name'] for t in self.translations]


def merge_responses(responses: [TranslationResponse]) -> TranslationResponse:
    new_translations = []
    money_costs = 0

    for response in responses:
        new_translations = merge_translations(new_translations, response.translations)
        money_costs += response.costs.money

    return TranslationResponse(
        translations=new_translations,
        costs=TranslationCosts(
            money=money_costs
        )
    )


def merge_translations(translations1: [dict], translations2: [dict]) -> [dict]:
    return merge_unique(translations1, translations2,
                        lambda t1, t2: t1['translation'].lower() == t2['translation'].lower())


def make_translation(translation: str, quality: int, service_name: str) -> dict:
    return dict(
        translation=translation,
        quality=quality,
        service_name=service_name
    )
