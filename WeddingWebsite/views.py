import os
from pathlib import Path
from random import choice

from .models import RSVP, RegistryEntry, Thread, Post, CustomUser, PostVersion
from .forms import ThreadForm, CustomUserForm, RSVPForm, PostVersionForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.text import slugify

from django.views.generic import View, ListView, CreateView
from django.views.generic.base import TemplateView

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    """
    View for the home page.
    """
    template_name = "home.html"


class InfoPageView(LoginRequiredMixin, TemplateView):
    """
    View for the informational page.
    """
    template_name = "info.html"


class RSVPPageView(LoginRequiredMixin, CreateView):
    """
    View that shows the RSVP form.
    """
    model = RSVP
    form_class = RSVPForm
    template_name = "rsvp.html"
    success_url = reverse_lazy("home")

    def get(self, *args, **kwargs):
        # if the user has already rsvp'd then don't want them to be able to rsvp again
        if self.request.user.rsvp:
            return redirect('home')
        return super().get(*args, **kwargs)
    
    def form_valid(self, form):
        # save the RSVP object with form.save(), then add that object to the appropriate user (one-to-one)
        self.object = form.save()
        user = self.request.user
        user.rsvp = self.object
        user.save()
        return super().form_valid(form)
    

class PasswordChangeSuccessView(TemplateView):
    """
    View after successfully changing your password.
    """
    template_name = "password_change_success.html"


class LogoutView(View):
    """
    Logout view.    
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home"))
    

class RegistryListView(LoginRequiredMixin, ListView):
    """
    Main registry view that shows all the items.
    """
    template_name = "registry.html"
    model = RegistryEntry
    context_object_name = "registry_items"
    # we want the unreservable items at the bottom
    ordering = "-is_reservable"


class RegistryPostView(LoginRequiredMixin, View):
    """
    View when a user reserves an item.
    """
    def post(self, request):
        reg_entry = RegistryEntry.objects.get(id=request.POST['item_id'])

        # user unreserves an item
        if reg_entry.reserved_by == request.user:
            reg_entry.reserved_by = None
            reg_entry.save()
        # user reserves an item
        elif not reg_entry.reserved_by:  
            reg_entry.reserved_by = request.user
            reg_entry.save()
        
        return HttpResponseRedirect(reverse("registry"))


class ThreadListView(LoginRequiredMixin, ListView):
    """
    View that shows all the forum threads.
    """
    template_name = "forum.html"
    model = Thread
    context_object_name = "threads"
    paginate_by = 10
    ordering = ['creation_time']


class PostListView(LoginRequiredMixin, ListView):
    """
    View for a single thread.
    """
    template_name = "thread.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 10
    # always order by when posts were created
    ordering = ['id']

    def post(self, request, threadslug):
        # create a new Post object
        new_post = Post()

        # assign it the current user and thread
        user = request.user
        new_post.creator = user
        new_post.thread = Thread.objects.get(slug=threadslug)

        new_post.save()

        # create a new PostVersion object
        new_postversion = PostVersion()

        # assign it the text of the post and the new Post object
        new_postversion.text = request.POST['text']
        new_postversion.post = new_post

        new_postversion.save()

        # go back to the new post's thread
        return redirect(new_post.thread)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # add a PostVersionForm context to every page in the thread
        form = PostVersionForm()
        context['form'] = form
        return context

    def get_queryset(self):
        # only show the posts with thread_id of the current thread
        current_thread = Thread.objects.get(slug=self.kwargs['threadslug'])
        base_query = super().get_queryset()
        data = base_query.filter(thread=current_thread)
        return data
    

class CreateThreadView(LoginRequiredMixin, TemplateView):
    """
    View for creating a new thread.
    """
    template_name = "create_thread.html"

    def get_context_data(self, **kwargs):
        # add a ThreadForm context to the view
        context =  super().get_context_data(**kwargs)
        form = ThreadForm()
        context['form'] = form
        return context
    
    def post(self, request):
        user = request.user
 
        # create a new Thread object and assign it a title, creator, and slug
        new_thread = Thread()
        new_thread.title = request.POST['title']
        new_thread.creator = user
        new_thread.slug = slugify(new_thread.title)
        new_thread.save()

        # create a new Post object and assign it a creator and the new Thread object as its thread
        first_post = Post()
        first_post.creator = user
        first_post.thread = new_thread
        first_post.save()

        '''create a new PostVersion object and assign it the text of the post 
        and assign it the new Post object as its post'''
        new_postversion = PostVersion()
        new_postversion.text = request.POST['first_post']
        new_postversion.post = first_post

        new_postversion.save()

        # go back to the main forum page
        return redirect("forum")
    

class EditPostView(LoginRequiredMixin, TemplateView):
    """
    View for editing a post.
    """
    template_name = "edit_post.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['threadslug'] = self.kwargs['threadslug']
        context['post_id'] = self.kwargs['id']
        # the most recent postversion text is what we want to display for a post
        context['post_text'] = Post.objects.get(id=self.kwargs['id']).postversion_set.last().text

        return context

    def get(self, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        # users can only get to their own posts
        if post.creator != self.request.user:
            return redirect('home')

        return super().get(*args, **kwargs)

    def post(self, request, threadslug, id):
        post = Post.objects.get(id=id)

        # users can only edit their own posts
        if post.creator == request.user:
            current_text = post.postversion_set.last().text
            new_post_text = request.POST['post_text']
            # only save if the new text is different from the old text
            if current_text != new_post_text: 
                new_postversion = PostVersion()
                new_postversion.text = new_post_text
                new_postversion.post = post

                new_postversion.save()
                # mark the post as edited
                post.edited = True
                post.save()
            
            return redirect(post.thread)
       
        return redirect('home')


class ChangeProfilePic(LoginRequiredMixin, TemplateView):
    """
    View for changing a user's profile picture.
    """
    template_name = "profile_pic.html"

    @staticmethod
    # after a user changes their profile picture, delete the unused pictures
    def delete_unused_profile_pics():
        # get a list of all the current user images
        customuser_images = [Path(object.profile_pic.url).name for object in CustomUser.objects.all()]
        profile_pics_path = os.path.join(settings.BASE_DIR, "uploads", "profile_pics")

        for image in os.scandir(profile_pics_path):
            try:
                # if the image is not used
                if image.name not in customuser_images and os.path.isfile(image.path):
                    os.remove(image.path)
            # if two users change their pictures at the same time
            except FileNotFoundError:  
                pass
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # add a CustomUserForm context to access the user's profile picture
        form = CustomUserForm()
        context['form'] = form
        return context
    
    def post(self, request):
        user = request.user
        # update the user's CustomUser object
        form = CustomUserForm(request.POST, request.FILES, instance=user)
 
        if form.is_valid():
            form.save()
        
        self.delete_unused_profile_pics()
        # go back to the profile-pic page
        return reverse("change-profile-pic")
    

class AccountInfoView(LoginRequiredMixin, TemplateView):
    """
    View for selecting Change Password, Change Profile Picture, or Logout.
    """
    template_name = "account_info.html"


# directory where different pet images for the 404 page are stored
PET_DIR = os.path.join(settings.BASE_DIR, "WeddingWebsite", "static", "pet_images")
PET_IMAGES = [str(image.name) for image in os.scandir(PET_DIR)]

def error_404(request, *args, **kwargs):
    """
    Custom 404 page shows a random pet image each time.
    """
    random_pet = choice(PET_IMAGES)

    return render(request, 
                "404.html", 
                {"random_image": f"pet_images/{random_pet}"}, 
                status=404
            )
