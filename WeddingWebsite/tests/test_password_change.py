from django.test import SimpleTestCase
from django.urls import reverse


class PasswordChangeSuccessPageTests(SimpleTestCase):
    """
    Class to test how the Password Change Success page loads.
    """
    def test_page_loads(self):
        """
        Test if the Password Change Success page loads correctly if going to the page's URL.
        """
        response = self.client.get("/password-change-success")
        self.assertEqual(response.status_code, 200)

    def test_page_loads_using_url_name(self):
        """
        Test if the Password Change Success page loads correctly using the name of the URL.
        """
        response = self.client.get(reverse("password-change-success"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        Test what template the Password Change Success page uses.
        """
        response = self.client.get(reverse("password-change-success"))
        self.assertTemplateUsed(response, "password_change_success.html")

    def test_template_content(self):
        """
        Test the content of the template used for the Password Change Success page.
        """
        response = self.client.get(reverse("password-change-success"))
        self.assertContains(response, "successfully")
