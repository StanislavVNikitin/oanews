from django.shortcuts import render
from django.views.generic import ListView

from .models import Category, Post


class Home(ListView):
    model = Post
    template_name = "blog/blog.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Органические ацидурии"
        return context
