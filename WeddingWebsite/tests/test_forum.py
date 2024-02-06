from django.test import TestCase, Client
from django.urls import reverse
from WeddingWebsite.models import CustomUser, Thread, Post, PostVersion
from model_bakery import baker
from django.utils import timezone


class ForumPageTests(TestCase):
    """
    Class to test how the forum pages load or redirect.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user, log them in, and create a test thread with a test post.
        """
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')
        cls.thread = baker.make(Thread, title="Test Thread", slug="test-thread")
        cls.post = baker.make(Post, id=999, thread=cls.thread, creator=cls.user)
        cls.postversion = baker.make(PostVersion, text="Test"*100, creation_time=timezone.now, post=cls.post)

    def test_page_loads_if_logged_in(self):
        """
        Test if the forum, test thread, and Edit Post pages load correctly for a logged-in user.
        """
        response = self.cli.get("/forum")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get("/forum/test-thread")
        self.assertEqual(response.status_code, 200)
        response = self.cli.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertEqual(response.status_code, 200)
    
    def test_page_redirects_if_not_logged_in(self):
        """
        Test if the forum, test thread, and Edit Post redirect for 
        a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get("/forum")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get("/forum/test-thread")
        self.assertEqual(response.status_code, 302)
        response = self.cli.get(reverse("forum"))
        self.assertEqual(response.status_code, 302)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertEqual(response.status_code, 302)

    def test_template_used_if_logged_in(self):
        """
        Test what template the forum and Edit Post pages use
        for a logged-in user.
        """
        response = self.cli.get(reverse("forum"))
        self.assertTemplateUsed(response, "forum.html")

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertTemplateUsed(response, "edit_post.html")

    def test_template_used_if_not_logged_in(self):
        """
        Test what template the forum and Edit Post pages use
        for a user who is not logged in.
        """
        self.cli.logout()
        response = self.cli.get(reverse("forum"))
        self.assertTemplateNotUsed(response, "forum.html")

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertTemplateNotUsed(response, "edit_post.html")

    def test_template_content(self):
        """
        Test the content of the templates used for a logged-in user on the 
        forum, test thread, and Edit Post pages.
        """
        response = self.cli.get(reverse("forum"))
        self.assertContains(response, "Test Thread")
        response = self.cli.get("/forum/test-thread")
        self.assertContains(response, "Test"*100)

        response = self.cli.get(reverse("edit-post", args=["test-thread", "999"]))
        self.assertContains(response, "Edit Post")


class ForumPostTests(TestCase):
    """
    Class to test how a user could try to edit a post.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user, log them in, and create a test thread with a test post.
        """
        cls.cli = Client()
        cls.user = CustomUser.objects.create_user(username='testuser', password='12345')
        cls.cli.login(username='testuser', password='12345')
        cls.thread = baker.make(Thread, title="Test Thread", slug="test-thread")
        cls.post = baker.make(Post, id=999, thread=cls.thread, creator=cls.user)
        cls.postversion = baker.make(PostVersion, text="Test"*100, creation_time=timezone.now, post=cls.post)
        
    def test_user_editing_post_when_logged_in(self):
        """
        Test if a logged-in user edits a post that they are redirected back to the 
        thread with that post and that their edited post is displayed.
        """
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
        """
        Test if a user who is not logged in tries to submit a POST request to edit
        a post that they are redirected to the login page.
        """
        self.cli.logout()
        response = self.cli.post(
            reverse("edit-post", args=["test-thread", "999"]), 
            data={'post_text': "text text text",},
        )
        self.assertRedirects(
            response, 
            expected_url="/login?next=/forum/test-thread/999/edit",
            status_code=302,
            target_status_code=200,
        )


class ForumModelTests(TestCase):
    """
    Class to test the Thread, Post, and PostVersion models.    
    """
    @classmethod
    def setUpTestData(cls):
        """
        Create a test thread with a test post.
        """
        cls.thread = baker.make(Thread, title="Test Thread", slug="test-thread")
        cls.post = baker.make(Post, id=999, thread=cls.thread)
        cls.postversion = baker.make(PostVersion, text="Test"*100, post=cls.post)

    def test_number_thread_instances(self):
        """
        Test creating many Thread objects.
        """
        threads = baker.make(Thread, _quantity=20)
        assert len(threads) == 20

    def test_number_post_instances(self):
        """
        Test creating many Post objects.
        """
        posts = baker.make(Post, thread=self.thread, _quantity=100)
        assert len(posts) == 100

    def test_number_postversion_instances(self):
        """
        Test creating many PostVersion objects.
        """
        postversions = baker.make(PostVersion, post=self.post, _quantity=15)
        assert len(postversions) == 15

    def test_thread_get_absolute_url(self):
        """
        Test to ensure the get_absolute_url method of the Thread model
        returns the correct url.
        """
        assert self.thread.get_absolute_url() == "/forum/test-thread"

    def test_thread_str_method(self):
        """
        Test to ensure the __str__ method of the Thread model is working.
        """
        assert self.thread.__str__() == "Test Thread"

    def test_post_str_method(self):
        """
        Test to ensure the __str__ method of the Post model is working.
        """
        assert self.post.__str__() == "999"

    def test_postversion_str_method(self):
        """
        Test to ensure the __str__ method of the PostVersion model is working.
        """
        assert self.postversion.__str__() == "Test"*100