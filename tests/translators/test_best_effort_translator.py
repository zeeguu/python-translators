from unittest import TestCase

from python_translators.translation_query import TranslationQuery
from python_translators.translators.best_effort_translator import (
    DummyBestEffortTranslator,
    BestEffortTranslator,
)


class TestBestEffortTranslator(TestCase):

    def setUp(self):
        self.translator = DummyBestEffortTranslator(
            source_language="de", target_language="en"
        )
        self.bet = BestEffortTranslator(source_language="de", target_language="en")

    def testEnsureDifferentWordThanOriginalReturnedIfPossible(self):
        response = self.translator.translate(
            TranslationQuery(query="ada", max_translations=1)
        )

        self.assertNotEqual(response.translations[0]["translation"], "ada")

    def testEnsureContextualHasPriority(self):
        response = self.bet.translate(
            TranslationQuery(
                before_context="Hunderte Züge und Dutzende Flüge wurden ",
                query="gestrichen",
                after_context=" .",
                max_translations=3,
            )
        )

        assert response.translations[0]["translation"] == "cancelled"

    def test_issue_20__avoidance_of_suspiciously_long_translations(self):
        # source of example:
        # http://www.spiegel.de/lebenundlernen/job/equal-pay-day-warum-die-deutschen-nicht-ueber-geld-reden-a-1198494.html
        response = self.bet.translate(
            TranslationQuery(
                before_context="Der amerikanische Traum wurzelt in dem Glauben, dass der ",
                query="Einzelne",
                after_context=" es vom Tellerwäscher zum Milliardär schaffen kann.",
                max_translations=3,
            )
        )

        # this works only after we 'half' the importance of the Google -- with context which
        # translated more than the actual query normally
        # [{'translation': 'individual', 'service_name': 'Microsoft - with context', 'quality': 75},
        # {'translation': 'Single', 'service_name': 'Google - without context', 'quality': 70},
        # {'translation': 'individual can make', 'quality': 40, 'service_name': 'Google - with context'}]
        assert response.translations[0]["translation"] in ["individual", "individuals"]

    def test_issue_41__avoidance_of_empty_strings(self):
        # source of example:
        # http://www.spiegel.de/panorama/justiz/indiana-bankraeuber-kam-mit-dem-taxi-a-1198724.html
        response = self.bet.translate(
            TranslationQuery(
                before_context="Nach der Fahrt zu der Bank ",
                query="schob",
                after_context=' er dem Angestellten an der Kasse lediglich einen Zettel zu: "Dies ist ein Überfall.',
                max_translations=3,
            )
        )

        assert response.translations[0]["translation"] != ""
