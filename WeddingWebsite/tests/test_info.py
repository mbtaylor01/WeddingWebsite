from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser


class InfoPageTests(TestCase):
    """
    Class to test how the Info page loads or redirects.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and log them in.
        """
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_page_loads_if_logged_in(self):
        """
        Test if the Info page loads correctly for a logged-in user.
        """
        response = self.cli.get("/info")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("info"))
        self.assertEqual(response.status_code, 200)

    def test_page_redirects_if_not_logged_in(self):
        """
        Test if the Info page redirects for a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get("/info")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("info"))
        self.assertEqual(response.status_code, 302)
       
    def test_template_used_if_logged_in(self):
        """
        Test what template the Info page uses for a logged-in user.
        """
        response = self.cli.get(reverse("info"))
        self.assertTemplateUsed(response, "info.html")

    def test_template_used_if_not_logged_in(self):
        """
        Test what template the Info page uses for a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get(reverse("info"))
        self.assertTemplateNotUsed(response, "info.html")

    def test_template_content(self):
        """
        Test the content of the template used for a logged-in user.
        """
        response = self.cli.get(reverse("info"))
        self.assertContains(response, "Information")