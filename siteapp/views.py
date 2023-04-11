from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView
from django.core.mail import send_mail
from .forms import ContactForm, MyUserStoreForm, ChangePublicUserStoreForm
from .models import Page, MenuHome, UserStore
from django.contrib import messages
from django.conf import settings
from pytils.translit import slugify
from django.db.models import Q


# Create your views here.
class Home(ListView):
    model = Page
    template_name = "siteapp/index.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        context['title'] = "Органические ацидемии"
        context['description'] = "Главная страница "
        return context

    def get_queryset(self):
        return get_object_or_404(Page, slug='home')


class PageView(DetailView):
    model = Page
    template_name = "siteapp/page.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        self.object.views = F('views')  + 1
        self.object.save()
        self.object.refresh_from_db()
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

class UserStoreDetail(LoginRequiredMixin, DetailView):
    model = UserStore
    template_name = "siteapp/userstore.html"
    context_object_name = "userstore"

    def get_queryset(self):
        return UserStore.objects.filter(Q(deleted=False, is_published=True, is_moderated=True) | Q(deleted=False, user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        self.object.views = F('views')  + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

class UserStoreList(LoginRequiredMixin, ListView):
    model = UserStore
    template_name = "siteapp/userstore_list.html"
    context_object_name = "userstores"
    paginate_by = 6


    def get_queryset(self):
        return UserStore.objects.filter(deleted=False, is_published=True, is_moderated=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        context['title'] = "Истории семей"
        return context

class CreateMyUserStore(LoginRequiredMixin, CreateView):
    form_class = MyUserStoreForm
    template_name = "siteapp/my_userstore_create_and_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание пользовательской истории"
        context['menuhome'] = MenuHome.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.slug = slugify(self.object.title)
        subject_mail = f'Сайт OAnews.ru сообщение: Новая история на модерацию:  {self.object.title}'
        content_mail = f'На сайте добавлена новая история {self.object.title} нужно ее промодерировать.'
        self.object = self.object.save()
        mail = send_mail(subject_mail, content_mail, settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL_ADDRESS],fail_silently=True)
        return super().form_valid(form)

class MyUserStoreList(LoginRequiredMixin, ListView):
    model = UserStore
    template_name = "siteapp/my_userstore_list.html"
    context_object_name = "userstores"


    def get_queryset(self):
        return UserStore.objects.filter(deleted=False, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои истории'
        context['menuhome'] = MenuHome.objects.all()
        return context

class MyUserStoreDelete(DeleteView):
    model = UserStore
    template_name = 'siteapp/my_userstore_delete.html'
    success_url = reverse_lazy('siteapp:my_user_stores_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление истории'
        context['menuhome'] = MenuHome.objects.all()
        return context


class UpdateMyUserStore(LoginRequiredMixin, UpdateView):
    model = UserStore
    form_class = MyUserStoreForm
    template_name = "siteapp/my_userstore_create_and_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Изменение пользовательской истории"
        context['menuhome'] = MenuHome.objects.all()
        return context

    def form_valid(self, form):
        myuserstoreindb = UserStore.objects.get(pk=self.kwargs["pk"], user=self.request.user)
        if myuserstoreindb:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.slug = slugify(self.object.title)
            if not self.object.title == myuserstoreindb.title or not self.object.content == myuserstoreindb.content or not self.object.photo == myuserstoreindb.photo:
                self.object.is_moderated = False
            self.object = self.object.save()
            subject_mail = f'Сайт OAnews.ru сообщение: Измененная история на модерацию { myuserstoreindb.title}'
            content_mail = f'На сайте изменена история { myuserstoreindb.title} нужно ее промодерировать.'
            mail = send_mail(subject_mail, content_mail, settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL_ADDRESS], fail_silently=True)
            return super().form_valid(form)


class ChangePublicMyUserStore(LoginRequiredMixin, UpdateView):
    model = UserStore
    form_class = ChangePublicUserStoreForm
    template_name = "siteapp/my_userstore_change_is_published.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание пользовательской истории"
        context['menuhome'] = MenuHome.objects.all()
        context['userstorepublished'] = not UserStore.objects.get(pk=self.kwargs["pk"]).is_published
        return context
