from abc import ABCMeta, abstractmethod


class Translator(object):
    __metaclass__ = ABCMeta

    def __init__(self, source_language, target_language):
        self.source_language = source_language
        self.target_language = target_language

    @abstractmethod
    def translate(self, query, max_translations=1):
        pass
