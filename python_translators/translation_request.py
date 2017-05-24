class TranslationRequest(object):
    def __init__(self, query: str = '', before_context: str = '', after_context: str = '', max_translations: int = 1):
        self.query = query
        self.before_context = before_context
        self.after_context = after_context
        self.max_translations = max_translations

    def is_context_aware_request(self):
        return self.before_context or self.after_context
