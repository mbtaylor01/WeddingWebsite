from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser

class InfoPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_page_loads_if_logged_in(self):
        response = self.cli.get("/info")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("info"))
        self.assertEqual(response.status_code, 200)

    def test_page_redirects_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get("/info")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("info"))
        self.assertEqual(response.status_code, 302)
       
    def test_template_used_if_logged_in(self):
        response = self.cli.get(reverse("info"))
        self.assertTemplateUsed(response, "info.html")

    def test_template_used_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get(reverse("info"))
        self.assertTemplateNotUsed(response, "info.html")

    def test_template_content(self):
        response = self.cli.get(reverse("info"))
        self.assertContains(response, "Information")