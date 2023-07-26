from django import forms
from .models import Thread, Post, CustomUser
from django.forms import ModelForm, Textarea

class ThreadForm(forms.ModelForm):
    first_post = forms.CharField(max_length=5000, widget=Textarea)

    class Meta:
        model = Thread
        fields = ['title']
        # labels = {
        #     "text": "Your Name:",
        #     "review_text": "Your Feedback",
        #     "rating": "Your Rating",
        # }
        error_messages = {
            "title": {
                "required": "Thread title can't be blank.",
                "max_length": "Way too long; please shorten the title.",
            }
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

        labels = {
            "text": "Your Name:",
        }

        error_messages = {
            "text": {
                "required": "Please write something.",
                "max_length": "Way too long; please control yourself.",
            }
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_pic']
