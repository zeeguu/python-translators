SPANISH = 'es'
FRENCH = 'fr'
ITALIAN = 'it'
ENGLISH = 'en'

LANGUAGE_CODE_MAPPING = {
    SPANISH: 'spanish',
    FRENCH: 'french',
    ITALIAN: 'italian',
    ENGLISH: 'english'
}


def code_to_full_language(language_code):
    return LANGUAGE_CODE_MAPPING[language_code]
