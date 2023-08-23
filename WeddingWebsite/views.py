import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import RSVP, RegistryEntry, Thread, Post, CustomUser, PostVersion
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView
from .forms import ThreadForm, CustomUserForm, RSVPForm, PostVersionForm
from django.utils.text import slugify
from django.shortcuts import redirect
from pathlib import Path
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import View
from random import choice

PET_DIR = os.path.join(settings.BASE_DIR, "WeddingWebsite", "static", "pet_images")
PET_IMAGES = [str(image.name) for image in os.scandir(PET_DIR)]

class HomePageView(TemplateView):
    template_name = "home.html"


class InfoPageView(TemplateView):
    template_name = "info.html"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(InfoPageView, self).get(*args, **kwargs)


class RSVPPageView(CreateView):
    model = RSVP
    form_class = RSVPForm
    template_name = "rsvp.html"
    success_url = reverse_lazy("thankyou")

    def get(self, *args, **kwargs):
        # if the user has already rsvp'd then don't want them to be able to rsvp again
        if not self.request.user.is_authenticated or self.request.user.rsvp:
            return redirect('home')
        return super(RSVPPageView, self).get(*args, **kwargs)
    
    def form_valid(self, form):
        # save the object with form.save(), then add that object to the appropriate user (one-to-one)
        self.object = form.save()
        user = self.request.user
        user.rsvp = self.object
        user.save()
        return super().form_valid(form)


class ThankYouView(TemplateView):
    template_name = "thankyou.html"

class PasswordChangeSuccessView(TemplateView):
    template_name = "password_change_success.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home"))
    

class RegistryListView(ListView):
    template_name = "registry.html"
    model = RegistryEntry
    context_object_name = "registry_items"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(RegistryListView, self).get(*args, **kwargs)


class RegistryPostView(View):
    def post(self, request):
        reg_entry = RegistryEntry.objects.get(id=request.POST['item_id'])

        if reg_entry.reserved_by == request.user:  # the unreserve button
            reg_entry.reserved_by = None
            reg_entry.save()
        elif not reg_entry.reserved_by:  # the reserve button
            reg_entry.reserved_by = request.user
            reg_entry.save()
        else:  # the item is reserved, but the page still displays the reserve button
            return HttpResponseRedirect(reverse('thankyou'))
        
        return HttpResponseRedirect(reverse("registry"))


class ForumListView(ListView):
    template_name = "forum.html"
    model = Thread
    context_object_name = "threads"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(ForumListView, self).get(*args, **kwargs)


class ThreadListView(ListView):
    template_name = "thread.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 20
    ordering = ['id']  # always order by when posts were created

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(ThreadListView, self).get(*args, **kwargs)

    def post(self, request, threadslug):
        new_post = Post()
        user = request.user
        new_post.creator = user
        new_post.thread = Thread.objects.get(slug=threadslug)

        new_post.save()

        new_postversion = PostVersion()
        new_postversion.text = request.POST['text']
        new_postversion.post = new_post

        new_postversion.save()

        return redirect(new_post.thread)

    def get_context_data(self, **kwargs):  # add a postform context to every page in the thread
        context =  super().get_context_data(**kwargs)
        form = PostVersionForm()
        context['form'] = form
        return context

    def get_queryset(self):  # only show the posts with thread_id of the current thread
        current_thread = Thread.objects.get(slug=self.kwargs['threadslug'])
        base_query = super().get_queryset()
        data = base_query.filter(thread=current_thread)
        return data
    

class CreateThreadView(TemplateView):
    template_name = "create_thread.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        form = ThreadForm()
        context['form'] = form
        return context
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(CreateThreadView, self).get(*args, **kwargs)
    
    def post(self, request):
        user = request.user
 
        new_thread = Thread()
        new_thread.title = request.POST['title']
        new_thread.creator = user
        new_thread.slug = slugify(new_thread.title)
        new_thread.save()

        first_post = Post()
        first_post.creator = user
        first_post.thread = new_thread
        first_post.save()

        new_postversion = PostVersion()
        new_postversion.text = request.POST['first_post']
        new_postversion.post = first_post

        new_postversion.save()

        return redirect("forum")
    
class EditPostView(TemplateView):
    template_name = "edit_post.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['threadslug'] = self.kwargs['threadslug']
        context['post_id'] = self.kwargs['id']
        context['post_text'] = Post.objects.get(id=self.kwargs['id']).postversion_set.last().text
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        else:
            post = Post.objects.get(id=self.kwargs['id'])
            if post.creator != self.request.user: # users can only get to their own posts
                return redirect('home')

        return super(EditPostView, self).get(*args, **kwargs)

    def post(self, request, threadslug, id):
        if self.request.user.is_authenticated:
            post = Post.objects.get(id=id)
    
            # users can only edit their own posts
            if post.creator == request.user:
                current_text = post.postversion_set.last().text
                new_post_text = request.POST['post_text']
                
                if current_text != new_post_text: 
                    new_postversion = PostVersion()
                    new_postversion.text = new_post_text
                    new_postversion.post = post

                    new_postversion.save()

                    post.edited = True
                    post.save()
                
                return redirect(post.thread)
       
        return redirect('home')
        
    

class ChangeProfilePic(TemplateView):
    template_name = "profile_pic.html"

    @staticmethod
    def delete_unused_profile_pics():
        customuser_images = [Path(object.profile_pic.url).name for object in CustomUser.objects.all()]
        profile_pics_path = os.path.join(settings.BASE_DIR, "uploads", "profile_pics")
        for image in os.scandir(profile_pics_path):
            try:
                if image.name not in customuser_images and os.path.isfile(image.path):
                    os.remove(image.path)
            except FileNotFoundError:  # If two users change their pictures at the same time
                pass
        
    def get_context_data(self, **kwargs):  # add a postform context to every page in the thread
        context =  super().get_context_data(**kwargs)
        form = CustomUserForm()
        context['form'] = form
        return context
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        return super(ChangeProfilePic, self).get(*args, **kwargs)
    
    def post(self, request):
        user = request.user
        form = CustomUserForm(request.POST, request.FILES, instance=user)
 
        if form.is_valid():
            form.save()
        
        self.delete_unused_profile_pics()

        return redirect(user)
    

class AccountInfoView(TemplateView):
    template_name = "account_info.html"


def error_404(request, *args, **kwargs):
   random_pet = choice(PET_IMAGES)

   return render(request, 
                "404.html", 
                {"random_image": f"pet_images/{random_pet}"}, 
                status=404
            )


