from unittest import TestCase
from python_translators.query_processors.escape_html import EscapeHtml
from python_translators.translation_query import TranslationQuery


class TestCreateQueryForWordAndContext(TestCase):
    def setUp(self):
        self.query_processor = EscapeHtml()

    def test_word_at_the_end(self):

        query = TranslationQuery.for_word_occurrence(
            "for", "Det er der faktisk en simpel formel for."
        )
        self.assertEqual(query.before_context, "Det er der faktisk en simpel formel ")
        self.assertEqual(query.after_context, ".")
        self.assertEqual(query.query, "for")

    def test_word_in_the_middle(self):
        context = "Det er der faktisk en simpel formel for."
        word_str = "faktisk"

        query = TranslationQuery.for_word_occurrence(word_str, context)
        self.assertEqual(query.before_context, "Det er der ")
        self.assertEqual(query.query, "faktisk")
        print(query.after_context)
        self.assertEqual(query.after_context, " en simpel formel for.")
