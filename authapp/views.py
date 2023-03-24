import os

from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


from siteapp.models import MenuHome
from authapp.models import CustomUser


# Create your views here.

class Login(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context

class CustomPasswordChangeView(UserPassesTestMixin, PasswordChangeView):
    template_name = "registration/custom_password_change.html"
    success_url = reverse_lazy("authapp:password_change_done")

    def dispatch(self, request, *args, **kwargs):
        user_test_resul = self.get_test_func()()
        if not user_test_resul:
            return redirect(reverse_lazy('authapp:password_change', args=(self.request.user.id, )))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, message=f'Password has been successfully changed')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Изменить пароль"
        context['menuhome'] = MenuHome.objects.all()
        return context


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/custom_password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Имзенить пароль"
        context['menuhome'] = MenuHome.objects.all()
        return context


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile_edit.html"
    login_url = reverse_lazy("authapp:login")

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get("username"):
                request.user.username = request.POST.get("username")
            if request.POST.get("first_name"):
                request.user.first_name = request.POST.get("first_name")
            if request.POST.get("last_name"):
                request.user.last_name = request.POST.get("last_name")
            if request.POST.get("gender"):
                request.user.gender = request.POST.get("gender")
            if request.POST.get("birthday"):
                request.user.birthday = request.POST.get("birthday")
            if request.POST.get("weight"):
                request.user.weight = request.POST.get("weight")
            if request.POST.get("height"):
                request.user.height = request.POST.get("height")
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.FILES.get("avatar"):
                if request.user.avatar and os.path.exists(
                        request.user.avatar.path
                ):
                    os.remove(request.user.avatar.path)
                request.user.avatar = request.FILES.get("avatar")
            request.user.save()
            messages.add_message(request, messages.INFO, _("Saved!"))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{exp}"),
            )
        return HttpResponseRedirect(reverse_lazy("authapp:profile_edit"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        context['menuhome'] = MenuHome.objects.all()
        context['gender'] = CustomUser.GENGER_CHOICES
        return context