from unittest.mock import Mock, call

from django.test import Client, SimpleTestCase as TestCase

from search.manager import Results, SearchManager


class ManagerTestCase(TestCase):

    def test_it_exposes_an_index(self):
        test_manager = SearchManager(Mock())

        self.assertEqual(test_manager.index, {})

    def test_it_can_load_a_batch_of_documents(self):
        mock_mappings = Mock()
        mock_mappings.analyze = Mock(return_value=[])
        test_manager = SearchManager(mappings=mock_mappings)
        docs = [
            { 'name': 'test1', 'alt_name': 'test1.1', 'tz': 'America/Montreal' },
            { 'name': 'test2', 'alt_name': 'test2.1', 'tz': 'America/Montreal' },
        ]

        test_manager.bulk_add_documents(docs)

        expected_calls = [call(docs[0]), call(docs[1])]
        mock_mappings.analyze.assert_has_calls(expected_calls)
        self.assertEqual(test_manager.documents, docs)

    def test_it_stores_the_analyzed_tokens_in_the_index(self):
        mock_mappings = Mock()
        mock_analyze = Mock(side_effect = [
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


    def test_it_can_search_through_a_batch_of_documents(self):
        mock_mappings = Mock()
        test_manager = SearchManager(mappings=mock_mappings)
        matching_search_token = "anything"
        matching_document_index = 3
        test_manager.index = {
            matching_search_token: [matching_document_index],
            "thing": [2],
        }
        test_manager.documents = [
            {"test": 1},
            {"test": 3},
            {"test": 3},
            {"test": 3},
        ]

        results = test_manager.search(matching_search_token)

        self.assertEqual(results, [test_manager.documents[matching_document_index]])
