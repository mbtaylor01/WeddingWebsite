from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser, RSVP, RegistryEntry
from model_bakery import baker

class RegistryPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_page_loads_if_logged_in(self):
        response = self.cli.get("/registry")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("registry"))
        self.assertEqual(response.status_code, 200)
    
    def test_page_redirects_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get("/registry")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("registry"))
        self.assertEqual(response.status_code, 302)

    def test_template_used_if_logged_in(self):
        response = self.cli.get(reverse("registry"))
        self.assertTemplateUsed(response, "registry.html")

    def test_template_used_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get(reverse("registry"))
        self.assertTemplateNotUsed(response, "registry.html")

    def test_template_content(self):
        baker.make(RegistryEntry, title="registry_item_1", _create_files=True)
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "registry_item_1")
        self.assertContains(response, "Reserve")
        self.assertNotContains(response, "RESERVED - Click to Unreserve")
        baker.make(RegistryEntry, title="registry_item_2", reserved_by=self.user, _create_files=True)
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "RESERVED - Click to Unreserve")

class RegistryPostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_user_reserving_item_when_logged_in(self):
        response = self.cli.post(
            reverse("rsvp"), 
            data={
                "additional_people": "5",
                "allergies": "none",
                "alcohol": "test",
                "other": "testtesttest",
            },
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("thankyou"),
            status_code=302,
            target_status_code=200,
        )
        assert len(RSVP.objects.all()) == 1