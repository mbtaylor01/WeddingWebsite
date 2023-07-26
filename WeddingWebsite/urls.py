from .views import HomePageView, InfoPageView, rsvppage, ThankYouView, logout_view, AccountInfoView, RegistryListView
from .views import registry_post_page, ForumListView, ThreadListView, create_thread_page, ChangeProfilePic
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("info", InfoPageView.as_view(), name="info"),
    path("rsvp", rsvppage, name="rsvp"),
    path("thankyou", ThankYouView.as_view(), name="thankyou"),
    path("logout", logout_view, name="logout"),
    path("registry", RegistryListView.as_view(), name="registry"),
    path("reserve-item", registry_post_page, name="reserve-item"),
    path("forum", ForumListView.as_view(), name="forum"),
    path("forum/create-thread", create_thread_page, name="create-thread"),
    path("forum/<slug:threadslug>", ThreadListView.as_view(), name="thread"),
    path("account-info", AccountInfoView.as_view(), name="account-info"),
    path("profile-pic", ChangeProfilePic.as_view(), name="change-profile-pic"),

    path("change-password", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("home"), template_name="change_password.html"), name="change-password"),

    path("reset-password", auth_views.PasswordResetView.as_view(success_url=reverse_lazy("reset-password-sent")), name="reset-password"),
    path("reset-password-sent", auth_views.PasswordResetDoneView.as_view(), name="reset-password-sent"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("reset-password-success")), name="reset-password-confirm"),
    path("reset-password-success", auth_views.PasswordResetCompleteView.as_view(), name="reset-password-success"),
]