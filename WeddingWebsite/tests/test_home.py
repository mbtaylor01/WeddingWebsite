from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    """
    Class to test how the homepage loads and the 
    contents of the homepage.
    """
    def test_page_loads(self):
        """
        Test if the homepage loads correctly.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_page_loads_using_url_name(self):
        """
        Test if the homepage loads correctly using the URL name.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        Test what template the homepage uses.
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        """
        Test the content of the homepage.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "rsvp")
    