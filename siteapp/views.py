from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView

from .models import Page


# Create your views here.
class Home(ListView):
    model = Page
    template_name = "siteapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='home')
        return context


class PageView(TemplateView):
    model = Page
    template_name = "siteapp/page.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        print(slug)
        context['page'] = get_object_or_404(Page, slug=slug)
        return context


class ContactPage(ListView):
    model = Page
    template_name = "siteapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='contacts')
        return context