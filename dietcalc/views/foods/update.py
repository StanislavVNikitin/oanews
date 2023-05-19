__all__ = ["UpdateMyFood"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from siteapp.models import MenuHome
from dietcalc.forms import CreateAndUpdateMyFoodForm

from dietcalc.models import Food

class UpdateMyFood(LoginRequiredMixin, UpdateView):
    form_class = CreateAndUpdateMyFoodForm
    template_name = "dietcalc/foods/my_food_create.html"
    model = Food

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Food.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Обновление пользовательского продукта"
        context['button'] = "Сохранить"
        context['menuhome'] = MenuHome.objects.all()
        return context