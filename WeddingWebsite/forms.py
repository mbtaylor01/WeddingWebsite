from django import forms
from django.forms import Textarea
from .models import Thread, CustomUser, RSVP, PostVersion


class ThreadForm(forms.ModelForm):
    """
    Form for creating a thread.
    """
    # each thread must have at least one post
    first_post = forms.CharField(max_length=5000, widget=Textarea)

    class Meta:
        model = Thread
        fields = ['title']
        
        error_messages = {
            "title": {
                "required": "Thread title can't be blank.",
                "max_length": "Way too long; please shorten the title.",
            }
        }


class PostVersionForm(forms.ModelForm):
    """
    Form for creating a new version of a post.
    """
    class Meta:
        model = PostVersion
        fields = ['text']

        error_messages = {
            "text": {
                "required": "Please write something.",
                "max_length": "Way too long; please control yourself.",
            }
        }


class CustomUserForm(forms.ModelForm):
    """
    Form used for changing a user's profile picture.
    """
    class Meta:
        model = CustomUser
        fields = ['profile_pic']


class RSVPForm(forms.ModelForm):
    """
    Form for creating a RSVP entry.
    """
    class Meta:
        model = RSVP
        fields = '__all__'
        labels = {
            "party_size": "Size of your party (including yourself)?",
            "allergies": "Any food allergies?",
            "alcohol": "Favorite alcohol (we know you like tequila, Mom):",
            "other": "Anything else we should know?",
        }
          