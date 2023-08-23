from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from .models import CustomUser, Thread, Post, PostVersion, RSVP, RegistryEntry
from model_bakery import baker
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Create your tests here.
class HomePageTests(SimpleTestCase):
    def test_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_page_loads_using_url_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "rsvp")

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

class RSVPModelTests(TestCase):
    def test_number_instances_made(self):
        rsvps = baker.make(RSVP, _fill_optional=True, _quantity=100)
        assert len(rsvps) == 100

    def test_str_method_with_user(self):
        customuser = baker.make(CustomUser, _fill_optional=True)
        rsvp = baker.make(RSVP, customuser=customuser, _fill_optional=True,)
        assert "+" in rsvp.__str__()
        
    def test_str_method_without_user(self):
        rsvp = baker.make(RSVP, _fill_optional=True,)
        assert "+" not in rsvp.__str__() and "-" in rsvp.__str__()

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

class ForumPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')
        cls.thread = baker.make(Thread, title="Test Thread", slug="test-thread", creation_time=datetime.now().astimezone)
        cls.post = baker.make(Post, id=999, thread=cls.thread, creator=cls.user)
        cls.postversion = baker.make(PostVersion, text="Test"*100, creation_time=(datetime.now() - timedelta(days=7)).astimezone, post=cls.post)

    def test_page_loads_if_logged_in(self):
        response = self.cli.get("/forum")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get("/forum/test-thread")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertEqual(response.status_code, 200)
    
    def test_page_redirects_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get("/forum")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get("/forum/test-thread")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("forum"))
        self.assertEqual(response.status_code, 302)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertEqual(response.status_code, 302)

    def test_user_editing_post_when_logged_in(self):
        response = self.cli.post(
            reverse("edit-post", args=["test-thread", "999"]), 
            data={"post_text": "text text text",},
            follow=True,
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("thread", args=["test-thread",]),
            status_code=302,
            target_status_code=200,
        )
        self.assertContains(response, "text text text")

    def test_user_editing_post_when_not_logged_in(self):
        self.cli.logout()
        response = self.cli.post(
            reverse("edit-post", args=["test-thread", "999"]), 
            data={'post_text': "text text text",},
        )
        self.assertRedirects(
            response, 
            expected_url=reverse("home"),
            status_code=302,
            target_status_code=200,
        )
        
    def test_template_used_if_logged_in(self):
        response = self.cli.get(reverse("forum"))
        self.assertTemplateUsed(response, "forum.html")

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertTemplateUsed(response, "edit_post.html")

    def test_template_used_if_not_logged_in(self):
        self.cli.logout()
        response = self.cli.get(reverse("forum"))
        self.assertTemplateNotUsed(response, "forum.html")

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertTemplateNotUsed(response, "edit_post.html")

    def test_template_content(self):
        response = self.cli.get(reverse("forum"))
        self.assertContains(response, "Test Thread")
        response = self.cli.get("/forum/test-thread")
        self.assertContains(response, "Test"*100)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertContains(response, "Edit Post")

class ForumModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.thread = baker.make(Thread, title="Test Thread", slug="test-thread", creation_time=datetime.now().astimezone)
        cls.post = baker.make(Post, id=999, thread=cls.thread)
        cls.postversion = baker.make(PostVersion, text="Test"*100, creation_time=datetime.now().astimezone, post=cls.post)

    def test_number_thread_instances(self):
        threads = baker.make(Thread, creation_time=datetime.now().astimezone, _quantity=20)
        assert len(threads) == 20

    def test_number_post_instances(self):
        posts = baker.make(Post, thread=self.thread, _quantity=100)
        assert len(posts) == 100

    def test_number_postversion_instances(self):
        postversions = baker.make(PostVersion, creation_time=datetime.now().astimezone, post=self.post, _quantity=15)
        assert len(postversions) == 15

    def test_thread_get_absolute_url(self):
        assert self.thread.get_absolute_url() == "/forum/test-thread"

    def test_thread_str_method(self):
        assert self.thread.__str__() == "Test Thread"

    def test_post_str_method(self):
        assert self.post.__str__() == "999"

    def test_postversion_str_method(self):
        assert self.postversion.__str__() == "Test"*100

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

    