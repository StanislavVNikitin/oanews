from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Page, MenuHome
from django.contrib import messages
from django.conf import settings


# Create your views here.
class Home(ListView):
    model = Page
    template_name = "siteapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='home')
        context['menuhome'] = MenuHome.objects.all()
        return context


class PageView(TemplateView):
    model = Page
    template_name = "siteapp/page.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        print(slug)
        context['page'] = get_object_or_404(Page, slug=slug)
        context['menuhome'] = MenuHome.objects.all()
        return context


class ContactPage(ListView):
    model = Page
    template_name = "siteapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='contacts')
        context['menuhome'] = MenuHome.objects.all()
        return context

def contact_sendmail(request):
    page = get_object_or_404(Page, slug='contacts')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject_mail = f'Сайт OAnews.ru сообщение: {form.cleaned_data["subject"]}'
            content_mail = f'Вам отправлено письмо с формы обратной связи сайта Oanews.ru\nИмя отправителя: {form.cleaned_data["name"]}\nЕмаил: {form.cleaned_data["email"]}\nТема сообщения: {form.cleaned_data["subject"]}\nТекст сообщения: {form.cleaned_data["content"]}'
            mail = send_mail(subject_mail, content_mail, settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL_ADDRESS], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('siteapp:contacts')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'siteapp/contacts.html', {"form": form, "page": page, "menuhome": MenuHome.objects.all()})