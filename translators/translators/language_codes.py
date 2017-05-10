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


def code_to_full_language(language_code):
    if language_code not in LANGUAGE_CODE_MAPPING:
        raise Exception('This language code is not supported!')

    return LANGUAGE_CODE_MAPPING[language_code]
