""" Simple end to end tests to make sure everything chimes """
from unittest.mock import patch

from django.test import Client, SimpleTestCase as TestCase


class ViewsTestCase(TestCase):
    def setUp(self):
        self.test_client = Client()

    def test_suggestions_end_point(self):
        response = self.test_client.get('/suggestions', {'q': '6077243'})

        self.assertEqual(200, response.status_code)

    def test_suggestions_no_matches(self):
        response = self.test_client.get('/suggestions', {'q': 'asdflajsdflkjsadflkjsdflkjsdf'})

        self.assertEqual(200, response.status_code)
        self.assertEqual({'suggestions': []}, response.json())

    @patch('api.views.SEARCH_MANAGER.search')
    def test_suggestions_with_lng_lat(self, search_stub):
        response = self.test_client.get(
            '/suggestions',
            {
                'q': 'Albany',
                'latitude': '35.465438',
                'longitude': '-74.75623',
            }
        )

        search_stub.assert_called_once_with('Albany', ('35.465438', '-74.75623'))
        self.assertEqual(200, response.status_code)
