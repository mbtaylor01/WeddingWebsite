import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import RSVP, RegistryEntry, Thread, Post, CustomUser
from django.contrib.auth import logout
from django.views.generic import ListView
from .forms import ThreadForm, PostForm, CustomUserForm
from django.utils.text import slugify
from django.shortcuts import redirect
from pathlib import Path
from django.conf import settings
from django.views.generic.base import TemplateView

def homepage(request):
    return render(request, "home.html")

def infopage(request):
    return render(request, "info.html")

def rsvppage(request):
    if request.method == 'POST':
        rsvp_form = RSVP(
            full_name = request.POST['fullname'],
            additional_people = request.POST['additionals'],
            allergies = request.POST['allergies'],
            alcohol = request.POST['alcohol'],
            other = request.POST['other'],
            )
        rsvp_form.save()
        return HttpResponseRedirect(reverse("thankyou"))
    
    elif request.user.is_authenticated:
        return render(request, 'rsvp.html')
    else:
        return HttpResponseRedirect(reverse("home"))  # if someone tries to go to /rsvp directly

def thankyoupage(request):
    return render(request, 'thankyou.html')

def logout_view(request):
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


def registry_post_page(request):
    if request.method == 'POST':
        reg_entry = RegistryEntry.objects.get(id=request.POST['item_id'])

        if reg_entry.reserved_by == request.user.username:  # the unreserve button
            reg_entry.reserved_by = None
            reg_entry.save()
        elif not reg_entry.reserved_by:  # the reserve button
            reg_entry.reserved_by = request.user.username
            reg_entry.save()
        else:  # the item is reserved, but the page still displays the reserve button
            return HttpResponseRedirect(reverse('thankyou'))

    return HttpResponseRedirect(reverse('registry'))

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
    paginate_by = 5

    def post(self, request, threadslug):
        new_post = Post()
        new_post.text = request.POST['text']
        user = CustomUser.objects.get(username=request.user.username)
        new_post.creator = user
        new_post.thread = Thread.objects.get(slug=threadslug)

        new_post.save()

        return redirect(new_post.thread)

    def get_context_data(self, **kwargs):  # add a postform context to every page in the thread
        context =  super().get_context_data(**kwargs)
        form = PostForm()
        context['form'] = form
        return context

    def get_queryset(self):  # only show the posts with thread_id of the current thread
        the_thread = Thread.objects.get(slug=self.kwargs['threadslug'])

        base_query = super().get_queryset()
        data = base_query.filter(thread_id=the_thread.id)
        return data
    
def create_thread_page(request):
    if request.user.is_authenticated:
        if request.method == "GET":  # show the thread creation page
            form = ThreadForm()

            return render(request, "create_thread.html", {
                "form": form
            })
        else:  # create the thread object along with the first post of the thread
            user = CustomUser.objects.get(username=request.user.username)

            new_thread = Thread()
            new_thread.title = request.POST['title']
            new_thread.creator = user
            new_thread.slug = slugify(new_thread.title)
            new_thread.save()

            first_post = Post()
            first_post.text = request.POST['first_post']
            user = CustomUser.objects.get(username=request.user.username)
            first_post.creator = user
            first_post.thread = new_thread
            first_post.save()

    return HttpResponseRedirect(reverse("forum"))
    
class ChangeProfilePic(TemplateView):
    template_name = "profile_pic.html"

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
        user = CustomUser.objects.get(username=request.user.username)
        form = CustomUserForm(request.POST, request.FILES, instance=user)
 
        if form.is_valid():
            form.save()
        
        customuser_images = [Path(object.profile_pic.url).name for object in CustomUser.objects.all()]
        profile_pics_path = os.path.join(settings.BASE_DIR, "uploads", "profile_pics")
        for image in os.scandir(profile_pics_path):
            if image.name not in customuser_images and os.path.isfile(image.path):
                os.remove(image.path)
        return redirect(user)
    
class AccountInfoView(TemplateView):
    template_name = "account_info.html"
    


