import unittest
from unittest import TestCase
from translators.context_processors.remove_unnecessary_sentences import RemoveUnnecessarySentences


class TestRemoveUnnecessarySentences(TestCase):
    def setUp(self):
        self.context_processor = RemoveUnnecessarySentences(language_code='nl')

    def test_single_sentence(self):
        params = {
            'before_context': 'De directeur',
            'query': 'treedt',
            'after_context': ' af.'
        }

        results = self.context_processor.process_context(**params)

        self.assertEqual(params, results)

    def test_multiple_sentences(self):
        params = {
            'before_context': 'Justitieminister Koen Geens (CD&V) werkt aan een wetsontwerp dat burgerinfiltranten '
                              'mogelijk maakt in de strijd tegen',
            'query': 'terrorisme',
            'after_context': 'en georganiseerde misdaad. Dat zegt hij woensdag in Knack, nadat Brussels '
                             'procureur-generaal Johan Delmulle daar vorig najaar een lans voor had gebroken. '
                             'Daarnaast werkt Geens ook aan een regeling rond spijtoptanten. Een akkoord binnen de '
                             'meerderheid is er nog niet..'
        }

        results = self.context_processor.process_context(**params)

        self.assertEqual(results['before_context'], params['before_context'])  # before context should remain the same
        self.assertEqual(results['query'], params['query'])  # query should be untouched

        self.assertEqual(results['after_context'], 'en georganiseerde misdaad.')



if __name__ == '__main__':
    unittest.main()

