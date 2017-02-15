from abc import ABCMeta, abstractmethod


class Translator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def translate(self, query, source_language, target_language, max_translations=1):
        pass
