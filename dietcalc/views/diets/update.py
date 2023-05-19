__all__ = ["UpdateMyDiet", "ChangePublicMyUserDiet"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from siteapp.models import MenuHome
from dietcalc.forms import CreateAndUpdateMyDietForm, ChangePublicUserDietForm

from dietcalc.models import UserDiet


class UpdateMyDiet(LoginRequiredMixin, UpdateView):
    form_class = CreateAndUpdateMyDietForm
    template_name = "dietcalc/diets/my_diet_create.html"
    model = UserDiet

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserDiet.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Обновление пользовательской диеты"
        context['button'] = "Сохранить"
        context['menuhome'] = MenuHome.objects.all()
        return context

class ChangePublicMyUserDiet(LoginRequiredMixin, UpdateView):
    model = UserDiet
    form_class = ChangePublicUserDietForm
    template_name = "dietcalc/diets/my_userdiet_change_is_published.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserDiet.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Публикакция пользовательской диеты"
        context['menuhome'] = MenuHome.objects.all()
        context['userdietpublished'] = not UserDiet.objects.get(pk=self.kwargs["pk"]).is_published
        return context