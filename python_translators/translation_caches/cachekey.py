from python_translators.translation_query import TranslationQuery


class CacheKey(object):
    def __init__(self, query: TranslationQuery, source_language, target_language):
        self.query = query
        self.source_language = source_language
        self.target_language = target_language

    def __hash__(self):
        return hash((self.query.before_context,
                     self.query.query,
                     self.query.after_context,
                     self.source_language,
                     self.target_language))

    def __eq__(self, other: 'CacheKey'):
        return (self.query.before_context,
                self.query.query,
                self.query.after_context,
                self.source_language,
                self.target_language) == (other.query.before_context,
                                          other.query.query,
                                          other.query.after_context,
                                          other.source_language,
                                          other.target_language)

    def __ne__(self, other):
        return not (self == other)
