import unittest
from unittest import TestCase
from translators.context_processors.reduce_to_one_sentence import ReduceToOneSentence


class TestReduceToOneSentence(TestCase):
    def setUp(self):
        self.context_processor = ReduceToOneSentence()

    def test_single_sentence(self):
        params = {
            'before_context': 'De directeur ',
            'query': 'treedt',
            'after_context': ' af.'
        }

        results = self.context_processor.process_context(**params)

        self.assertEquals(params, results)

    def test_multiple_sentences(self):
        params = {
            'before_context': 'Justitieminister Koen Geens (CD&V) werkt aan een wetsontwerp dat burgerinfiltranten '
                              'mogelijk maakt in de strijd tegen ',
            'query': 'terrorisme',
            'after_context': ' en georganiseerde misdaad. Dat zegt hij woensdag in Knack, nadat Brussels '
                             'procureur-generaal Johan Delmulle daar vorig najaar een lans voor had gebroken. '
                             'Daarnaast werkt Geens ook aan een regeling rond spijtoptanten. Een akkoord binnen de '
                             'meerderheid is er nog niet..'
        }

        results = self.context_processor.process_context(**params)

        self.assertEquals(results['before_context'], params['before_context'])  # before context should remain the same
        self.assertEquals(results['query'], params['query'])  # query should be untouched

        self.assertEquals(results['after_context'], ' en georganiseerde misdaad.')


if __name__ == '__main__':
    unittest.main()
