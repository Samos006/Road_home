from django.urls import path
from users.views import (
    UserDetailView,
    UserRegisterView,
    UserLoginView,
    UserEditProfileView,
    UserChangePasswordView,
    UserLogoutView,
    GroupListView,
    GroupDetailView,
)

app_name = "users"

urlpatterns = [
    path("<int:user_id>/", UserDetailView.as_view(), name="user_detail"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("edit-profile/", UserEditProfileView.as_view(), name="edit_profile"),
    path("change-password/", UserChangePasswordView.as_view(), name="change_password"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("groups/<int:user_id>/", GroupDetailView.as_view(), name="group_detail"),
]
