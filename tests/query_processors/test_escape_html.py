from unittest import TestCase
from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.translation_query import TranslationQuery


class TestEscapeHtml(TestCase):
    def setUp(self):
        self.query_processor = EscapeHtml()

    def test_escaping(self):
        q = TranslationQuery(
            before_context='"Hello", ',
            query='said',
            after_context="the man."
        )

        result = self.query_processor.process_query(q)

        self.assertEqual(result.before_context, '&quot;Hello&quot;, ')

        # query and after_context should remain the same
        self.assertEquals(result.query, q.query)
        self.assertEquals(result.after_context, q.after_context)
