from django.test import SimpleTestCase as TestCase

from search.analyzers import (
    AutocompleteAnalyzer,
    KeywordAnalyzer,
    ListAnalyzer,
)


class KeywordAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = KeywordAnalyzer()

    def test_it_generates_one_token_only(self):
        tokens = self.analyzer.analyze("any thing at all")

        self.assertEqual(tokens, [("any thing at all", 1)])


class AutocompleteAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = AutocompleteAnalyzer()

    def test_it_generates_edge_grams_of_minimum_three_charachers(self):
        tokens = self.analyzer.analyze('Saint-Catherine Jacques Cartier bo')

        self.assertEqual([analysis[0] for analysis in tokens], [
            'saint-catherine jacques cartier bo',
            'sai',
            'sain',
            'saint',
            'cat',
            'cath',
            'cathe',
            'cather',
            'catheri',
            'catherin',
            'catherine',
            'jac',
            'jacq',
            'jacqu',
            'jacque',
            'jacques',
            'car',
            'cart',
            'carti',
            'cartie',
            'cartier',
            'bo',
        ])

class ListAnalyzerTestCase(TestCase):
    def setUp(self):
        self.analyzer = ListAnalyzer()

    def test_it_generates_keyword_tokens_for_each_item_in_list(self):
        tokens = self.analyzer.analyze(
            'edmundston,ehdmundston,edomonsuton,едмундстон,эдмундстон,اڈمنڈسٹن,エドモンストン'
        )

        self.assertEqual(tokens, [
            ('edmundston', 1.0),
            ('ehdmundston', 1.0),
            ('edomonsuton', 1.0),
            ('едмундстон', 1.0),
            ('эдмундстон', 1.0),
            ('اڈمنڈسٹن', 1.0),
            ('エドモンストン', 1.0),
        ])
