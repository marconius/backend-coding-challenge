from django.test import SimpleTestCase as TestCase

from search.analyzers import (
    AutocompleteAnalyzer,
    KeywordAnalyzer,
    ListAnalyzer,
    NoopAnalyzer,
)


class KeywordAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = KeywordAnalyzer()

    def test_it_generates_one_token_only(self):
        tokens = self.analyzer.analyze("any thing at all")

        self.assertEqual(tokens, ["any thing at all"])
