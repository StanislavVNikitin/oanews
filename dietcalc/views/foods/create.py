__all__ = ["CreateMyFood"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from siteapp.models import MenuHome
from dietcalc.forms import CreateAndUpdateMyFoodForm

class CreateMyFood(LoginRequiredMixin, CreateView):
    form_class = CreateAndUpdateMyFoodForm
    template_name = "dietcalc/foods/my_food_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление пользовательского продукта"
        context['button'] = "Добавить"
        context['menuhome'] = MenuHome.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)