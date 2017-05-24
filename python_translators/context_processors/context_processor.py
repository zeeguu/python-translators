from abc import ABCMeta, abstractmethod


class ContextProcessor(object, metaclass=ABCMeta):
    @abstractmethod
    def process_context(self, before_context: str, query: str, after_context: str):
        """
        Processes the context
        
        :param before_context: 
        :param query: 
        :param after_context: 
        :return: 
        """
        pass
