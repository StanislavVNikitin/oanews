from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import AuthappConfig

from .views import *

app_name = AuthappConfig.name

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/<int:pk>", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("profile_edit/", ProfileEditView.as_view(), name="profile_edit"),
]