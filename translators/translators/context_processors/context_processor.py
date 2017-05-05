from abc import ABCMeta, abstractmethod


class ContextProcessor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_context(self, before_context, query, after_context):
        pass
