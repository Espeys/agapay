from datetime import timedelta
from dateutil.parser import parse
from django.test import TestCase
from django.utils import timezone


class PingViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_success_scenario(self):
        start = timezone.localtime(timezone.now())
        end = start + timedelta(seconds=60)

        response = self.client.get('/api/v1/ping/')
        data = response.json()

        self.assertIn('success', data)
        self.assertIsInstance(data['success'], bool)
        self.assertTrue(data['success'])

        self.assertIn('errors', data)
        self.assertIsInstance(data['errors'], list)
        self.assertFalse(data['errors'])

        self.assertIn('data', data)
        self.assertTrue(start < parse(data['data']) < end)

    def test_failed_scenario(self):
        response = self.client.get('/api/v1/ping/', {'error': True})
        data = response.json()

        self.assertIn('success', data)
        self.assertIsInstance(data['success'], bool)
        self.assertFalse(data['success'])

        self.assertIn('errors', data)
        self.assertIsInstance(data['errors'], list)
        self.assertTrue(len(data['errors']) == 1)

        self.assertIn('data', data)
        self.assertIsNone(data['data'])

        error = data['errors'][0]

        self.assertIsInstance(error, dict)

        self.assertIn('field', error)
        self.assertIsInstance(error['field'], str)
        self.assertEqual(error['field'], 'error')

        self.assertIn('code', error)
        self.assertIsInstance(error['code'], int)

        self.assertIn('message', error)
        self.assertIsInstance(error['message'], str)
