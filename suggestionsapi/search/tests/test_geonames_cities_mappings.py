from unittest.mock import Mock, call

from django.test import Client, SimpleTestCase as TestCase

from search.geonames_cities_mappings import GeonamesCitiesMappings
from search.analyzers import (
    AutocompleteAnalyzer,
    KeywordAnalyzer,
    ListAnalyzer,
    NoopAnalyzer,
)


class MappingsTestCase(TestCase):
    def setUp(self):
        self.mock_analyzer_instance = Mock()
        self.mock_analyzer_instance.analyze = Mock(return_value=[])

        self.mappings = GeonamesCitiesMappings()

    def test_it_picks_an_analyzer_for_each_field_and_analyzes_the_value(self):
        self.mappings.get_analyzer = Mock(return_value=self.mock_analyzer_instance)

        self.mappings.analyze({'id': '12345', 'name': 'st-bruno'})

        expected_calls = [call('id'), call('name')]
        self.mappings.get_analyzer.assert_has_calls(expected_calls)


    def test_it_produces_a_list_of_tokens_for_each_field(self):
        expected_tokens = ["test123"]
        self.mock_analyzer_instance.analyze.return_value = expected_tokens
        self.mappings.get_analyzer = Mock(return_value=self.mock_analyzer_instance)

        tokens = self.mappings.analyze({'id': '12345'})

        self.assertEqual(tokens, expected_tokens)


    def test_it_chooses_the_right_analyzer_for_key_word_fields(self):
        keyword_fields = ['id', 'feat_class', 'feat_code', 'country']

        for field in keyword_fields:
            analyzer = self.mappings.get_analyzer(field)

            self.assertIsInstance(
                analyzer,
                KeywordAnalyzer,
                'for {}'.format(field)
            )

    def test_it_chooses_the_right_analyzer_for_autocomplete_fields(self):
        keyword_fields = ['name', 'ascii']

        for field in keyword_fields:
            analyzer = self.mappings.get_analyzer(field)

            self.assertIsInstance(
                analyzer,
                AutocompleteAnalyzer,
                'for {}'.format(field)
            )

    def test_if_chooses_list_analyzer_for_alt_name(self):
        analyzer = self.mappings.get_analyzer('alt_name')

        self.assertIsInstance(analyzer, ListAnalyzer)

    def test_if_chooses_to_not_analyze_lat_long(self):
        # geolocation for documents will be a separate concern
        keyword_fields = ['lat', 'long']

        for field in keyword_fields:
            analyzer = self.mappings.get_analyzer(field)

            self.assertIsInstance(analyzer, NoopAnalyzer)

    def test_if_does_not_analyze_some_fields(self):
        # geolocation for documents will be a separate concern
        # Others will be nice to haves
        keyword_fields = [
            'cc2',
            'admin1',
            'admin2',
            'admin3',
            'admin4',
            'population',
            'elevation',
            'tz',
            'modified_at',
        ]

        for field in keyword_fields:
            analyzer = self.mappings.get_analyzer(field)

            self.assertIsInstance(analyzer, NoopAnalyzer, 'for {}'.format(field))
