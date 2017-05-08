from configobj import ConfigObj
import os

CONFIG_FILE_PATH = '~/.config/translators.cfg'


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
