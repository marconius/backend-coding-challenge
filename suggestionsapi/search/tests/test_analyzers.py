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


class AutocompleteAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = AutocompleteAnalyzer()

    def test_it_generates_edge_grams_of_minimum_three_charachers(self):
        tokens = self.analyzer.analyze('Catherine Jacques Cartier bo')

        self.assertEqual(tokens, [
            'Cat',
            'Cath',
            'Cathe',
            'Cather',
            'Catheri',
            'Catherin',
            'Catherine',
            'Jac',
            'Jacq',
            'Jacqu',
            'Jacque',
            'Jacques',
            'Car',
            'Cart',
            'Carti',
            'Cartie',
            'Cartier',
            'bo'
        ])

class ListAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = ListAnalyzer()

    def test_it_generates_keyword_tokens_for_each_item_in_list(self):
        tokens = self.analyzer.analyze(
            'Edmundston,Ehdmundston,edomonsuton,Едмундстон,Эдмундстон,اڈمنڈسٹن,エドモンストン'
        )

        self.assertEqual(tokens, [
            'Edmundston',
            'Ehdmundston',
            'edomonsuton',
            'Едмундстон',
            'Эдмундстон',
            'اڈمنڈسٹن',
            'エドモンストン',
        ])
