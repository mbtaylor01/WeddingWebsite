from django.test import SimpleTestCase
from django.urls import reverse

class PasswordChangeSuccessPageTests(SimpleTestCase):
    def test_page_loads(self):
        response = self.client.get("/password-change-success")
        self.assertEqual(response.status_code, 200)

    def test_page_loads_using_url_name(self):
        response = self.client.get(reverse("password-change-success"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("password-change-success"))
        self.assertTemplateUsed(response, "password_change_success.html")

    def test_template_content(self):
        response = self.client.get(reverse("password-change-success"))
        self.assertContains(response, "successfully")
