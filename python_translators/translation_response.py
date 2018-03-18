import json

from python_translators.translation_costs import TranslationCosts
from python_translators.utils import merge_unique
from python_translators import logger


class TranslationResponse(object):
    def __init__(self, translations: [dict] = None, costs: TranslationCosts = None):
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

    def to_json(self) -> str:
        return json.dumps({
            'costs': {
                'money': self.costs.money,
                'time': self.costs.time
            },
            'translations': self.translations
        })


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


def order_by_quality(translations: [dict], query):
    _trans = []
    for x in translations:
        if _probably_low_quality(x, query.query):
            _trans.append(_update_quality(x, 0.5))
        else:
            _trans.append(x)

    # then we sort the translations based on their quality
    _trans = sorted(_trans, key=lambda x: x['quality'], reverse=True)

    return _trans


def _probably_low_quality(translation_dict, origin):
    translation = translation_dict['translation']
    translation_service = translation_dict['service_name']
    log_string = f'Decreasing quality for ({origin}-{translation}) by: {translation_service}'

    # first, if a translation is the same as the original word,
    # can't be that great of a translation, really

    if translation == origin:
        logger.info(log_string)
        return True

    # especially with GT-with context we get translations
    # which capture more words than in the origin...
    # most of the times, such a translation is of low quality

    words_in_translation = len(translation.split())
    words_in_origin = len(origin.split())

    if words_in_translation > words_in_origin + 1:
        logger.info(log_string)
        return True


def _update_quality(old_translation: dict, ratio: float) -> dict:
    return dict(
        translation=old_translation["translation"],
        quality=int(old_translation["quality"] * ratio),
        service_name=old_translation["service_name"]
    )
