from django.test import Client, TestCase


class CoreAPISmokeTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_dashboard_endpoint_returns_200(self):
		response = self.client.get('/api/core/dashboard/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('total_urls', response.json())

	def test_url_list_endpoint_returns_200(self):
		response = self.client.get('/api/core/url-list/')
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response.json(), list)
