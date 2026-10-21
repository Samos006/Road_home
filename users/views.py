from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from users.forms import (
    UserChangePasswordForm,
    UserEditForm,
    UserLoginForm,
    UserRegistrationForm,
)
from users.models import User


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "profile_user"
    pk_url_kwarg = "user_id"


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.object.id})


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.request.user.id})


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.request.user.id})


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = "users/change_password.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"user_id": self.request.user.id})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("animals:animal_list")


class GroupListView(ListView):
    model = User
    template_name = "users/group_list.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(role="shelter").order_by("-date_joined")


class GroupDetailView(DetailView):
    model = User
    template_name = "users/group_detail.html"
    context_object_name = "group"
    pk_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.filter(role="shelter")
