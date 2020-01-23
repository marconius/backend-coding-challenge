""" Simple end to end tests to make sure everything chimes """
from django.test import Client, SimpleTestCase as TestCase


class ViewsTestCase(TestCase):
    def setUp(self):
        self.test_client = Client()

    def test_suggestions_end_point(self):
        response = self.test_client.get('/suggestions', {'q': '6077243'})

        self.assertEqual(200, response.status_code)
