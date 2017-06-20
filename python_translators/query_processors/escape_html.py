from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.translation_query import TranslationQuery

import copy
import html


class EscapeHtml(QueryProcessor):
    def __init__(self):
        super(EscapeHtml, self).__init__(name='escape_html')

    def process_query(self, query: TranslationQuery) -> TranslationQuery:
        new_query = copy.copy(query)

        new_query.query = html.escape(new_query.query)
        new_query.before_context = html.escape(new_query.before_context)
        new_query.after_context = html.escape(new_query.after_context)

        return new_query
