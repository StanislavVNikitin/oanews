__all__ = ["CreateMyDiet"]

import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from pytils.translit import slugify

from siteapp.models import MenuHome
from dietcalc.forms import CreateAndUpdateMyDietForm

class CreateMyDiet(LoginRequiredMixin, CreateView):
    form_class = CreateAndUpdateMyDietForm
    template_name = "dietcalc/diets/my_diet_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание пользовательской диеты"
        context['button'] = "Добавить"
        context['menuhome'] = MenuHome.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.slug = slugify(self.object.name)[:90] + '-' + ''.join(
            random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        return super().form_valid(form)