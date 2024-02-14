from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser, RegistryEntry
from model_bakery import baker


class RegistryPageTests(TestCase):
    """
    Class to test how the Registry page loads or redirects.
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
        Test if the Registry page loads correctly for a logged-in user.
        """
        response = self.cli.get("/registry")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("registry"))
        self.assertEqual(response.status_code, 200)
    
    def test_page_redirects_if_not_logged_in(self):
        """
        Test if the Registry page redirects for a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get("/registry")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("registry"))
        self.assertEqual(response.status_code, 302)

    def test_template_used_if_logged_in(self):
        """
        Test what template the Registry page uses for a logged-in user.
        """
        response = self.cli.get(reverse("registry"))
        self.assertTemplateUsed(response, "registry.html")

    def test_template_used_if_not_logged_in(self):
        """
        Test what template the Registry page uses for a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get(reverse("registry"))
        self.assertTemplateNotUsed(response, "registry.html")

    def test_template_content(self):
        """
        Test the content of the template used for a logged-in user if there are
        registry items that are reserved and items that are unreserved.
        """
        baker.make(RegistryEntry, title="registry_item_1")
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "registry_item_1")
        self.assertContains(response, "Click here if bringing this item!")
        self.assertNotContains(response, "Click to unreserve.")
        baker.make(RegistryEntry, title="registry_item_2", reserved_by=self.user)
        response = self.cli.get(reverse("registry"))
        self.assertContains(response, "Click to unreserve.")


class RegistryPostTests(TestCase):
    """
    Class to test how a user could try to reserve a registry item.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and log them in.
        """
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_user_reserving_item_when_logged_in(self):
        """
        Test a Registry object being created in the database correctly and if 
        a logged-in user clicks the Reserve link on that item, they will be redirected
        to the Registry page with that item showing as reserved.
        """
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
        self.assertContains(response, "Click to unreserve.")

    def test_user_unreserving_item_when_logged_in(self):
        """
        Test a Registry object being created in the database correctly and if 
        a logged-in user clicks the Unreserve link on that item, they will be redirected
        to the Registry page with that item not showing as reserved.
        """
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
        self.assertNotContains(response, "Click to unreserve.")
        self.assertContains(response, "Click here if bringing this item!")

    def test_user_reserving_item_when_not_logged_in(self):
        """
        Test that if a user who is not logged in tries to submit a POST request
        reserving an item, it will not work and they will be redirected to the login page.
        """
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
        """
        Test that if a logged-in user submits a POST request to try to reserve
        an item another user has reserved, it will not work.
        """
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

        