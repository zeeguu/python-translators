from abc import ABCMeta, abstractmethod


class ContextProcessor(object, metaclass=ABCMeta):
    # TODO: explain why ContextProcessor is ABC
    @abstractmethod
    def process_context(self, before_context, query, after_context):
        pass
