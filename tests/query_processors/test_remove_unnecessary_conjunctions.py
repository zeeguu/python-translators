import unittest
from unittest import TestCase
from python_translators.query_processors.remove_unnecessary_conjunctions import RemoveUnnecessaryConjunctions
from python_translators.translation_query import TranslationQuery


class TestRemoveUnnecessaryConjunctions(TestCase):
    def setUp(self):
        self.query_processor = RemoveUnnecessaryConjunctions(['and', 'or', 'but'])

    def test_simple_case(self):
        q = TranslationQuery(
            before_context='It is sunny and Amsterdam is the',
            query='capital city',
            after_context='of the Netherlands but Groningen is more awesome.'
        )

        result = self.query_processor.process_query(q)

        self.assertEqual(result.before_context, 'Amsterdam is the')
        self.assertEqual(result.query, 'capital city')  # query is unchanged
        self.assertEqual(result.after_context, 'of the Nethderlands')


if __name__ == '__main__':
    unittest.main()
