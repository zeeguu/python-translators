import os

from configobj import ConfigObj

# Configuration information is required by several of the translation
# APIs in the form of API keys. Several of the keys are:

# - WORDNIK_API_KEY
# - MICROSOFT_TRANSLATE_API_KEY
# - GOOGLE_TRANSLATE_API_KEY

# These keys are looked up in the following locations in order:
# 1. as environment variables
# 2. as constants defined in a config file specified by tne envvar TRANSLATORS_CONFIG_PATH
# 3. in the default location ~/.config/translators.cfg

# Finally, the keys can also be passed as arguments to the constructors of the
# corresponding translators


CONFIG_FILE_PATH = '~/.config/translators.cfg'
CONFIG_FILE_ENVIRON_VAR = 'TRANSLATORS_CONFIG_PATH'


def get_key_from_config(key_name):
    if key_name in os.environ:
        return os.environ[key_name]

    try:

        if CONFIG_FILE_ENVIRON_VAR in os.environ:
            config_file = os.environ[CONFIG_FILE_ENVIRON_VAR]
        else:
            config_file = os.path.expanduser(CONFIG_FILE_PATH)

        config = ConfigObj(config_file)
        key = config[key_name]
        return key
    except KeyError:
        raise Exception('No config file found. Create config file or pass key as argument to constructor')
