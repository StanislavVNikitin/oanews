from django.urls import path

from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("page/<str:slug>/", PageView.as_view(), name="page_slug"),
]
