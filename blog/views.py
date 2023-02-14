from django.shortcuts import render
from django.views.generic import ListView

from .models import Post


class Home(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Органические ацидурии"
        return context


def index(request):
    return render(request, "blog/index.html")


def get_category(request, slug):
    return render(request, "blog/category.html")


def get_post(request, slug):
    return render(request, "blog/category.html")
