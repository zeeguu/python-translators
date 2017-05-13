import unittest
from unittest import TestCase
from translators.context_processors.remove_unnecessary_conjunctions import RemoveUnnecessaryConjunctions


class TestRemoveUnnecessaryConjunctions(TestCase):
    def setUp(self):
        self.context_processor = RemoveUnnecessaryConjunctions(['and', 'or', 'but'])

    def test_simple_case(self):
        params = {
            'before_context': 'It is sunny and Amsterdam is the',
            'query': 'capital city',
            'after_context': 'of the Netherlands but Groningen is more awesome.',
        }

        results = self.context_processor.process_context(**params)

        self.assertEquals(results['before_context'], 'Amsterdam is the')
        self.assertEquals(results['query'], 'capital city')  # query is unchanged
        self.assertEquals(results['after_context'], 'of the Netherlands')

if __name__ == '__main__':
    unittest.main()
