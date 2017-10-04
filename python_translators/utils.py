"""
A file containing some utility functions used across the project
"""
import time
from configobj import ConfigObj
import os
import copy

CONFIG_FILE_PATH = '~/.config/translators.cfg'


def current_milli_time():
    return int(round(time.time() * 1000))


def get_key_from_config(key_name):

    if key_name in os.environ:
        return os.environ[key_name]

    try:
        config_file = os.path.expanduser(CONFIG_FILE_PATH)
        config = ConfigObj(config_file)
        key = config[key_name]
        return key
    except KeyError:
        raise Exception('No config file found. Create config file or pass key as argument to constructor')


# Language codes according to ISO 639-1
CZECH = 'cs'
DANISH = 'da'
DUTCH = 'nl'
ENGLISH = 'en'
ESTONIAN = 'et'
FINNISH = 'fi'
FRENCH = 'fr'
GERMAN = 'de'
GREEK = 'el'
ITALIAN = 'it'
NORWEGIAN = 'no'
POLISH = 'pl'
PORTUGUESE = 'pt'
SLOVENE = 'sl'
SPANISH = 'es'
SWEDISH = 'sv'
TURKISH = 'tr'

LANGUAGE_CODE_MAPPING = {
    CZECH: 'czech',
    DANISH: 'danish',
    DUTCH: 'dutch',
    ENGLISH: 'english',
    ESTONIAN: 'estonian',
    FINNISH: 'finnish',
    FRENCH: 'french',
    GERMAN: 'german',
    GREEK: 'greek',
    ITALIAN: 'italian',
    NORWEGIAN: 'norwegian',
    POLISH: 'polish',
    PORTUGUESE: 'portuguese',
    SLOVENE: 'slovene',
    SPANISH: 'spanish',
    SWEDISH: 'swedish',
    TURKISH: 'turkish'
}


# maps language codes to full language names
def code_to_full_language(language_code: str) -> str:
    if language_code not in LANGUAGE_CODE_MAPPING:
        raise Exception('This language code is not supported!')

    return LANGUAGE_CODE_MAPPING[language_code]


def merge_unique(arr1: [], arr2: [], eq) -> []:
    """
    Merges two arrays. The new array will not contain duplicates. This function runs in O(N^2). Do not use for large
    lists. Equality is defined by the function `eq`. `eq` should be a function that takes two parameters. If the two
    arguments passed to `eq` are considered equal, return true. Otherwise return false.
    :param arr1:
    :param arr2:
    :param eq:
    :return:
    """

    new_arr = copy.copy(arr1)

    for a2 in arr2:
        for a1 in arr1:
            if eq(a1, a2):
                break
        else:
            new_arr.append(a2)

    return new_arr


#def merge_translations(translations1: [], translations2: [[]]):
#    return merge_unique(translations1, translations2, lambda x, y: x.lower() == y.lower())


def format_dict_for_logging(d: dict) -> str:
    return '\n' + '\n'.join(f'\t{key}: {value}' for key, value in d.items())

