from django import forms
from .models import Thread, Post, CustomUser, RSVP
from django.forms import Textarea

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


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = '__all__'
        labels = {
            "full_name": "Full Name:",
            "additional_people": "How many people will you be bringing?",
            "allergies": "Any food allergies?",
            "alcohol": "Favorite alcohol (we know you like Tequila mom):",
            "other": "Anything else we should know?",
        }
          