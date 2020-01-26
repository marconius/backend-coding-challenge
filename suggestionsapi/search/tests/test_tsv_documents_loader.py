""" We are using django test framework for convenience,
but the `search` package is meant to be framework-agnostic,
so probably best to use a different test lib
"""
from django.test import SimpleTestCase as TestCase

from search.tsv_documents_loader import TsvDocumentsLoader


class TsvDocumentsLoaderTestCase(TestCase):

    def test_it_loads_data_from_path(self):
        test_loader = TsvDocumentsLoader(
            '/home/baba/workspace/backend-coding-challenge/suggestionsapi/' +
            'search/tests/fake_cities_canada-usa.tsv'
        )
        test_loader.load_documents()

        self.assertEqual(test_loader.documents[0]['name'], 'Montréal')
        self.assertEqual(test_loader.documents[1]['feat_code'], 'PPLA')
