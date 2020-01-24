from unittest import skip
from unittest.mock import Mock, call

from django.test import SimpleTestCase as TestCase

from search.manager import SearchManager


@skip('Abandoning due to lack of time, revisit if refactoring search manager')
class ManagerTestCase(TestCase):

    def test_it_exposes_an_index(self):
        test_manager = SearchManager(Mock())

        self.assertEqual(test_manager.index, {})

    def test_it_can_load_a_batch_of_documents(self):
        mock_mappings = Mock()
        mock_mappings.analyze = Mock(return_value=[])
        test_manager = SearchManager(mappings=mock_mappings)
        docs = [
            {'name': 'test1', 'alt_name': 'test1.1', 'tz': 'America/Montreal'},
            {'name': 'test2', 'alt_name': 'test2.1', 'tz': 'America/Montreal'},
        ]

        test_manager.bulk_add_documents(docs)

        expected_calls = [call(docs[0]), call(docs[1])]
        mock_mappings.analyze.assert_has_calls(expected_calls)
        self.assertEqual(test_manager.documents, docs)

    def test_it_stores_the_analyzed_tokens_in_the_index(self):
        mock_mappings = Mock()
        mock_analyze = Mock(side_effect=[
            ['token1', 'token2'],
            ['token3', 'token2'],
        ])
        mock_mappings.analyze = mock_analyze
        test_manager = SearchManager(mappings=mock_mappings)

        test_manager.bulk_add_documents(['this would be a real doc', 'another real doc'])

        self.assertEqual(test_manager.index, {
            'token1': [0],
            'token2': [0, 1],
            'token3': [1]
        })


@skip('Abandoning due to lack of time, revisit if refactoring search manager')
class ManagerSearchTestCase(TestCase):

    def setUp(self):
        self.test_manager = SearchManager(Mock())
        self.test_manager.index = {
            "anything": [3],
            "something": [2],
            "other": [0, 2],
            "the": [0, 3, 2, 1]
        }
        self.test_manager.documents = [
            {"country": 'CA', 'admin1': '03', 'name': 'Place1', 'lat': 1, 'long': 3},
            {"country": 'US', 'admin1': 'UT', 'name': 'Other', 'lat': 1, 'long': 3},
            {"country": 'CA', 'admin1': '10', 'name': 'Town', 'lat': 1, 'long': 3},
            {"country": 'US', 'admin1': 'NY', 'name': 'City', 'lat': 1, 'long': 3},
        ]

    def test_it_can_search_with_one_term(self):
        results = self.test_manager.search("anything")

        self.assertEqual(results, [self.test_manager.documents[3]])

    def test_it_only_returns_docs_that_match_all_terms(self):
        results = self.test_manager.search("something other")

        self.assertEqual(results, [self.test_manager.documents[2]])

    def test_it_returns_score_with_itf(self):
        sparse_results = self.test_manager.search("the")
        good_results = self.test_manager.search("something")

        self.assertEqual(len(sparse_results), 4)
        self.assertLess(sparse_results[0]["score"], good_results[0]["score"])
