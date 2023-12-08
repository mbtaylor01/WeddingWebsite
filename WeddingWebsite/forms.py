from django import forms
from .models import Thread, Post, CustomUser, RSVP, PostVersion
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

class PostVersionForm(forms.ModelForm):
    class Meta:
        model = PostVersion
        fields = ['text']

        # labels = {
        #     "text": "Post Text:",
        # }

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
            "party_size": "Size of your party (including yourself)?",
            "allergies": "Any food allergies?",
            "alcohol": "Favorite alcohol (we know you like tequila, Mom):",
            "other": "Anything else we should know?",
        }
          