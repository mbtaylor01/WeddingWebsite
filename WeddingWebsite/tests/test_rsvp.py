from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser, RSVP
from model_bakery import baker

class RSVPPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_page_loads_if_logged_in(self):
        response = self.cli.get("/rsvp")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("rsvp"))
        self.assertEqual(response.status_code, 200)
    
    def test_page_redirects_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get("/rsvp")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("rsvp"))
        self.assertEqual(response.status_code, 302)

    def test_template_used_if_logged_in(self):
        response = self.cli.get(reverse("rsvp"))
        self.assertTemplateUsed(response, "rsvp.html")

    def test_template_used_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get(reverse("rsvp"))
        self.assertTemplateNotUsed(response, "rsvp.html")

    def test_template_content(self):
        response = self.cli.get(reverse("rsvp"))
        self.assertContains(response, "allergies")

class RSVPPostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')

    def test_user_rsvping_when_logged_in(self):
        response = self.cli.post(
            reverse("rsvp"), 
            data={
                "party_size": "5",
                "allergies": "none",
                "alcohol": "test",
                "other": "testtesttest",
            },
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("home"),
            status_code=302,
            target_status_code=200,
        )
        assert len(RSVP.objects.all()) == 1

    def test_user_rsvping_when_not_logged_in(self):
        self.cli.logout()
        response = self.cli.post(
            reverse("rsvp"), 
            data={
                "party_size": "5",
                "allergies": "none",
                "alcohol": "test",
                "other": "testtesttest",
            },
        )
        self.assertRedirects(
            response, 
            expected_url="/login?next=/rsvp",
            status_code=302,
            target_status_code=200,
        )
        assert len(RSVP.objects.all()) == 0

    def test_user_rsvping_with_bad_data(self):
        response = self.cli.post(
            reverse("rsvp"), 
            data={
                "party_size": "string",
                "alcohol": "test",
                "other": "testtesttest",
            },
        )
        self.assertTemplateNotUsed(response, "home.html")
        self.assertTemplateUsed(response, "rsvp.html")
        assert len(RSVP.objects.all()) == 0

class RSVPModelTests(TestCase):
    def test_number_instances_made(self):
        rsvps = baker.make(RSVP, _fill_optional=True, _quantity=100)
        assert len(rsvps) == 100

    def test_str_method(self):
        customuser = baker.make(CustomUser, _fill_optional=True)
        rsvp = baker.make(RSVP, customuser=customuser, _fill_optional=True,)
        try:
            int(rsvp.__str__())
        except ValueError:
            assert False
