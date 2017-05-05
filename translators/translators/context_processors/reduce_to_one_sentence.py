from context_processor import ContextProcessor


class ReduceToOneSentence(ContextProcessor):
    def __init__(self, sentence_separator='. '):
        self.sentence_separator = sentence_separator

    def _process_before_context(self, before_context):
        k = before_context.rfind(self.sentence_separator)

        if k != -1:  # if there was a separator found
            return before_context[k:]

        return before_context

    def _process_after_context(self, after_context):
        k = after_context.find(self.sentence_separator)

        if k != -1:  # if there was a separator found
            return after_context[:(k+1)]

        return after_context

    def process_context(self, before_context, query, after_context):
        return {
            'before_context': self._process_before_context(before_context),
            'query': query,
            'after_context': self._process_after_context(after_context)
        }
