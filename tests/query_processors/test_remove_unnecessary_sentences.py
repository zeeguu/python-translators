import unittest
from unittest import TestCase
from python_translators.query_processors.remove_unnecessary_sentences import RemoveUnnecessarySentences
from python_translators.translation_query import TranslationQuery


class TestRemoveUnnecessarySentences(TestCase):
    def setUp(self):
        self.query_processor = RemoveUnnecessarySentences(language_code='nl')

    def test_single_sentence(self):
        q = TranslationQuery(
            before_context='De directeur',
            query='treedt',
            after_context=' af.'
        )

        result = self.query_processor.process_query(q)

        self.assertEqual(q, result)

    def test_multiple_sentences(self):
        query = TranslationQuery(
            before_context='Justitieminister Koen Geens (CD&V) werkt aan een wetsontwerp dat burgerinfiltranten '
                           'mogelijk maakt in de strijd tegen',
            query='terrorisme',
            after_context='en georganiseerde misdaad. Dat zegt hij woensdag in Knack, nadat Brussels '
                          'procureur-generaal Johan Delmulle daar vorig najaar een lans voor had gebroken. '
                          'Daarnaast werkt Geens ook aan een regeling rond spijtoptanten. Een akkoord binnen de '
                          'meerderheid is er nog niet..'
        )

        result = self.query_processor.process_query(query)

        self.assertEqual(query.before_context, result.before_context)  # before context should remain the same
        self.assertEqual(query.query, result.query)  # query should be untouched
        self.assertEqual(result.after_context, 'en georganiseerde misdaad.')

if __name__ == '__main__':
    unittest.main()

