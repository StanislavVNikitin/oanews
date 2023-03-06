from django.urls import path
from .apps import BlogConfig

from .views import *

app_name = BlogConfig.name

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("category/<str:slug>", PostByCategory.as_view(), name="category"),
    path("tag/<str:slug>", PostByTag.as_view(), name="tag"),
    path("post/<str:slug>", GetPost.as_view(), name="post"),
    path("search/", Search.as_view(), name="search"),
]
