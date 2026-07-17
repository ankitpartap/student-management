from django.test import TestCase
from django.urls import reverse


class StudentAppViewsTests(TestCase):
    def test_home_page_is_available(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
