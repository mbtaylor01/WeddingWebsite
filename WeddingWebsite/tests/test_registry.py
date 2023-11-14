from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser, RegistryEntry
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
        baker.make(RegistryEntry, title="registry_item_1")
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "registry_item_1")
        self.assertContains(response, "Reserve")
        self.assertNotContains(response, "Reserved! Click to unreserve.")
        baker.make(RegistryEntry, title="registry_item_2", reserved_by=self.user)
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "Reserved! Click to unreserve.")

class RegistryPostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_user_reserving_item_when_logged_in(self):
        baker.make(RegistryEntry, id=1, title="registry_item_1")
        response = self.cli.post(
            reverse("reserve-item"), 
            data={"item_id": "1",},
            follow=True
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("registry"),
            status_code=302,
            target_status_code=200,
        )
        self.assertContains(response, "Reserved! Click to unreserve.")

    def test_user_unreserving_item_when_logged_in(self):
        baker.make(RegistryEntry, id=1, title="registry_item_1", reserved_by=self.user)
        response = self.cli.post(
            reverse("reserve-item"), 
            data={"item_id": "1",},
            follow=True
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("registry"),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotContains(response, "Reserved! Click to unreserve.")
        self.assertContains(response, "Reserve")

    def test_user_reserving_item_when_not_logged_in(self):
        self.cli.logout()
        response = self.cli.post(
            reverse("reserve-item"), 
            data={"item_id": "1",},
        )
        self.assertRedirects(
            response, 
            expected_url="/login?next=/reserve-item",
            status_code=302,
            target_status_code=200,
        )

    def test_user_reserving_another_users_item(self):
        user = CustomUser.objects.create_user(username='testuser2', password='12345')
        baker.make(RegistryEntry, id=1, title="registry_item_1", reserved_by=user)
        response = self.cli.post(
            reverse("reserve-item"), 
            data={"item_id": "1",},
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("registry"),
            status_code=302,
            target_status_code=200,
        )

        